# -*- coding: utf-8 -*-
# Copyright: (c) 2026
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
name: jira_assets
short_description: Inventory source for Jira Assets (CMDB) objects via AQL
description:
  - Builds inventory from Jira Assets objects returned by an AQL query.
  - Requires a configuration file ending in C(jira_assets.yml) or C(jira_assets.yaml).
  - Uses the Assets REST API C(POST /object/aql) endpoint.
  - Flattens nested Assets attributes into snake_case host variables.
  - Supports constructed inventory features (C(compose), C(groups), C(keyed_groups))
    and optional caching.
version_added: "1.0.0"
options:
  plugin:
    description: Token that ensures this is a source file for the plugin.
    required: true
    choices: ["jira_assets"]
  cloud_id:
    description: Atlassian Cloud site ID used in the Assets API base URL.
    type: str
    required: true
    env:
      - name: JIRA_CLOUD_ID
  workspace_id:
    description: Jira Assets workspace ID.
    type: str
    required: true
    env:
      - name: JIRA_WORKSPACE_ID
  email:
    description:
      - Atlassian account email for basic authentication with an API token.
      - Required together with O(api_token) when O(bearer_token) is not set.
    type: str
    required: false
    env:
      - name: JIRA_EMAIL
  api_token:
    description:
      - Atlassian API token for basic authentication.
      - Required together with O(email) when O(bearer_token) is not set.
    type: str
    required: false
    env:
      - name: JIRA_API_TOKEN
  bearer_token:
    description:
      - OAuth 2.0 Bearer token.
      - When set, takes precedence over O(email) / O(api_token) basic auth.
    type: str
    required: false
    env:
      - name: JIRA_BEARER_TOKEN
  aql_query:
    description: Assets Query Language (AQL) filter used to select objects.
    type: str
    required: true
  max_results:
    description:
      - Page size for Assets API pagination.
      - Values of 1000 or higher can make C(isLast) unreliable; prefer 999 or lower.
    type: int
    default: 50
  include_attributes:
    description: Whether to request object attribute values from the API.
    type: bool
    default: true
  hostname_source:
    description:
      - Attribute name used as the inventory hostname.
      - Accepts the Assets display name (for example C(Name)) or its snake_case form
        (for example C(name)).
    type: str
    default: Name
  columns:
    description:
      - List of attribute names to expose as host variables.
      - Accepts Assets display names or snake_case forms.
      - When empty, all flattened attributes (plus system fields) are exposed.
    type: list
    elements: str
    default: []
  lowercase_hostname:
    description: Convert the inventory hostname to lowercase.
    type: bool
    default: false
extends_documentation_fragment:
  - constructed
  - inventory_cache
"""

EXAMPLES = r"""
# Minimal example — all hosts from objectType Server
plugin: jira_assets
# Prefer env vars: JIRA_CLOUD_ID, JIRA_WORKSPACE_ID, JIRA_EMAIL, JIRA_API_TOKEN
aql_query: "objectType = Server"

# Map attributes, group by type/OS, and set ansible_host
plugin: jira_assets
aql_query: "objectType = Server AND Status = Active"
hostname_source: Name
columns:
  - Name
  - IP Address
  - OS
  - Status
  - Environment
keyed_groups:
  - key: object_type
    prefix: jira_type
  - key: os | default('unknown', true) | replace(' ', '_') | lower
    prefix: jira_os
compose:
  ansible_host: ip_address | default(omit)
  ci_name: name
cache: true
cache_plugin: ansible.builtin.jsonfile
cache_timeout: 3600
cache_connection: /tmp/jira_assets_cache
cache_prefix: jira_assets
"""

import base64
import json
import re

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.module_utils.common.text.converters import to_native, to_text
from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable, Constructable

from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def to_snake_case(name):
    """Normalize an Assets attribute name to a snake_case hostvar key."""
    if name is None:
        return ""
    text = to_text(name).strip()
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text)
    return text.strip("_").lower()


def _truthy_flag(value, default=True):
    """Coerce API boolean-ish fields (bool or string) to bool."""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return to_text(value).strip().lower() in ("true", "1", "yes")


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "jira_assets"

    def verify_file(self, path):
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(("jira_assets.yaml", "jira_assets.yml")):
                return True
            self.display.vvv(
                'Skipping due to inventory source not ending in '
                '"jira_assets.yaml" nor "jira_assets.yml"'
            )
        return False

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache=cache)
        self._read_config_data(path)
        self._validate_auth()

        cache_key = self.get_cache_key(path)
        user_cache_setting = self.get_option("cache")
        # cache=True (default) means prefer reading from cache when enabled.
        # cache=False (e.g. --flush-cache) forces a remote refresh.
        attempt_to_read_cache = user_cache_setting and cache
        cache_needs_update = user_cache_setting and not cache

        results = None
        if attempt_to_read_cache:
            try:
                results = self._cache[cache_key]
            except KeyError:
                cache_needs_update = True

        if results is None:
            results = self._fetch_flattened_objects()
            # Persist a freshly fetched result set when caching is enabled.
            if user_cache_setting:
                cache_needs_update = True

        if cache_needs_update:
            self._cache[cache_key] = results

        self._populate(results)

    def _validate_auth(self):
        bearer = self.get_option("bearer_token")
        email = self.get_option("email")
        api_token = self.get_option("api_token")
        if bearer:
            return
        if email and api_token:
            return
        raise AnsibleParserError(
            "Authentication required: set bearer_token (or JIRA_BEARER_TOKEN), "
            "or both email and api_token (or JIRA_EMAIL and JIRA_API_TOKEN)."
        )

    def _auth_headers(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        bearer = self.get_option("bearer_token")
        if bearer:
            headers["Authorization"] = "Bearer {0}".format(bearer)
            return headers

        email = self.get_option("email")
        api_token = self.get_option("api_token")
        token = base64.b64encode(
            to_text("{0}:{1}".format(email, api_token)).encode("utf-8")
        ).decode("ascii")
        headers["Authorization"] = "Basic {0}".format(token)
        return headers

    def _api_url(self, start_at, max_results, include_attributes):
        cloud_id = self.get_option("cloud_id")
        workspace_id = self.get_option("workspace_id")
        query = urlencode(
            {
                "startAt": start_at,
                "maxResults": max_results,
                "includeAttributes": str(include_attributes).lower(),
            }
        )
        return (
            "https://api.atlassian.com/ex/jira/{cloud_id}/jsm/assets/workspace/"
            "{workspace_id}/v1/object/aql?{query}"
        ).format(
            cloud_id=cloud_id,
            workspace_id=workspace_id,
            query=query,
        )

    def _request_page(self, start_at):
        url = self._api_url(
            start_at=start_at,
            max_results=self.get_option("max_results"),
            include_attributes=self.get_option("include_attributes"),
        )
        body = json.dumps({"qlQuery": self.get_option("aql_query")}).encode("utf-8")
        # data= implies POST
        request = Request(url, data=body, headers=self._auth_headers())
        try:
            with urlopen(request, timeout=60) as response:
                payload = response.read()
        except HTTPError as exc:
            detail = ""
            try:
                detail = to_text(exc.read())
            except Exception:
                detail = to_native(exc)
            raise AnsibleError(
                "Jira Assets API HTTP {0} for {1}: {2}".format(exc.code, url, detail)
            )
        except URLError as exc:
            raise AnsibleError(
                "Jira Assets API connection error for {0}: {1}".format(
                    url, to_native(exc.reason)
                )
            )

        try:
            return json.loads(to_text(payload))
        except ValueError as exc:
            raise AnsibleError(
                "Jira Assets API returned invalid JSON: {0}".format(to_native(exc))
            )

    def _fetch_flattened_objects(self):
        start_at = 0
        max_results = self.get_option("max_results")
        all_entries = []
        attr_map = {}

        while True:
            page = self._request_page(start_at)
            # POST /object/aql uses "values"; tolerate legacy "objectEntries".
            entries = page.get("values")
            if entries is None:
                entries = page.get("objectEntries") or []

            page_attr_defs = page.get("objectTypeAttributes") or []
            attr_map.update(self._build_attribute_map(page_attr_defs))

            all_entries.extend(entries)

            is_last = _truthy_flag(page.get("isLast"), default=True)
            if is_last or not entries:
                break

            start_at += max_results

        return [self._flatten_object(entry, attr_map) for entry in all_entries]

    @staticmethod
    def _build_attribute_map(object_type_attributes):
        attr_map = {}
        for attr_def in object_type_attributes or []:
            attr_id = to_text(attr_def.get("id", ""))
            attr_name = attr_def.get("name")
            if attr_id and attr_name:
                attr_map[attr_id] = attr_name
        return attr_map

    def _flatten_object(self, entry, attr_map):
        record = {
            "object_id": to_text(entry.get("id", "")),
            "object_key": entry.get("objectKey") or "",
            "label": entry.get("label") or entry.get("name") or "",
            "created": entry.get("created") or "",
            "updated": entry.get("updated") or "",
            "object_type": (entry.get("objectType") or {}).get("name") or "",
        }

        for attribute in entry.get("attributes") or []:
            attr_type_id = to_text(attribute.get("objectTypeAttributeId", ""))
            raw_name = attr_map.get(attr_type_id)
            if not raw_name:
                raw_name = "attr_{0}".format(attr_type_id or "unknown")
            key = to_snake_case(raw_name)
            values = attribute.get("objectAttributeValues") or []
            record[key] = self._extract_attribute_value(values)

        return record

    @staticmethod
    def _extract_attribute_value(values):
        extracted = []
        for value in values:
            if not isinstance(value, dict):
                continue
            if value.get("displayValue") is not None:
                extracted.append(to_text(value.get("displayValue")))
            elif value.get("value") is not None:
                extracted.append(to_text(value.get("value")))
            elif value.get("referencedObject"):
                ref = value["referencedObject"]
                extracted.append(
                    to_text(ref.get("label") or ref.get("name") or ref.get("objectKey") or "")
                )

        if not extracted:
            return ""
        if len(extracted) == 1:
            return extracted[0]
        return ", ".join(extracted)

    def _resolve_hostname_key(self, hostname_source, record):
        candidates = []
        normalized = to_snake_case(hostname_source)
        if hostname_source:
            candidates.append(hostname_source)
        if normalized:
            candidates.append(normalized)

        for key in candidates:
            if key in record:
                return key

        # Allow common aliases used in compose examples.
        aliases = {
            "name": ["name", "label"],
            "label": ["label", "name"],
            "object_key": ["object_key"],
        }
        for alias in aliases.get(normalized, []):
            if alias in record:
                return alias
        return None

    @staticmethod
    def _column_keys(columns, record):
        if not columns:
            return list(record.keys())
        # Prefer snake_case keys for hostvars; Assets objects may omit empty attrs.
        return [to_snake_case(column) for column in columns]

    def _populate(self, records):
        hostname_source = self.get_option("hostname_source")
        lowercase = self.get_option("lowercase_hostname")
        columns = self.get_option("columns") or []
        compose = self.get_option("compose")
        groups = self.get_option("groups")
        keyed_groups = self.get_option("keyed_groups")
        strict = self.get_option("strict")

        for record in records:
            host_key = self._resolve_hostname_key(hostname_source, record)
            if not host_key:
                raise AnsibleParserError(
                    "Inventory hostname source '{0}' is not present in the record "
                    "for object_key={1}.".format(
                        hostname_source, record.get("object_key", "<unknown>")
                    )
                )

            inventory_hostname = record.get(host_key)
            if not inventory_hostname:
                self.display.warning(
                    "Skipping object {0} due to empty {1}".format(
                        record.get("object_key") or record.get("object_id"),
                        hostname_source,
                    )
                )
                continue

            inventory_hostname = to_text(inventory_hostname)
            if lowercase:
                inventory_hostname = inventory_hostname.lower()

            host = self.inventory.add_host(inventory_hostname)
            for key in self._column_keys(columns, record):
                self.inventory.set_variable(host, key, record.get(key, ""))

            self._set_composite_vars(compose, record.copy(), host, strict=strict)
            self._add_host_to_composed_groups(groups, record.copy(), host, strict=strict)
            self._add_host_to_keyed_groups(
                keyed_groups, record.copy(), host, strict=strict
            )
