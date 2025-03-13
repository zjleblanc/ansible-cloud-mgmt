#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2017, John Westcott IV <john.westcott.iv@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule, env_fallback

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'], 'supported_by': 'community'}


DOCUMENTATION = '''
---
module: export
author: "John Westcott IV (@john-westcott-iv)"
version_added: "3.7.0"
short_description: export resources from Automation Platform Controller.
description:
    - Export assets from Automation Platform Controller.
options:
requirements:
  - "awxkit >= 9.3.0"
notes:
  - Specifying a name of "all" for any asset type will export all items of that asset type.
extends_documentation_fragment: awx.awx.auth
'''

EXAMPLES = '''
- name: Export all assets
  inventory_dynamic:
'''

import logging
import requests

def __map_to_cac(inventory):
    cac = {
        "name": inventory['name'],
        "kind": inventory['kind'],
        "organization": inventory['summary_fields']['organization']['name'],
        "prevent_instance_group_fallback": inventory['prevent_instance_group_fallback'],
        "variables": inventory['variables']
    }

    if inventory['kind'] == 'smart':
        cac['host_filter'] = inventory['host_filter']
    if inventory.get('instance_groups', None):
        cac['instance_groups'] = inventory['instance_groups']
    if inventory.get('input_inventories', None):
        cac['input_inventories'] = inventory['input_inventories']

    return cac

def __get_related(host, token, resource):
    url = "https://" + host + resource
    res = requests.get(url, headers={"Authorization": "Bearer " + token})
    names = map(lambda resource: resource['name'], res.json()['results'])
    return list(names)

def __get_inventories(host, token):
    url = "https://" + host + "/api/v2/inventories/"
    res = requests.get(url, headers={"Authorization": "Bearer " + token})
    inventories_raw = res.json()['results']

    for inv in inventories_raw:
        if inv['related'].get('instance_groups', None):
            inv['instance_groups'] = __get_related(host, token, inv['related']['instance_groups'])
        if inv['related'].get('input_inventories', None):
            inv['input_inventories'] = __get_related(host, token, inv['related']['input_inventories'])

    inventories = map(__map_to_cac, inventories_raw)
    return list(inventories)

def main():
    argument_spec = dict(
        controller_host=dict(required=False, aliases=['tower_host'], fallback=(env_fallback, ['CONTROLLER_HOST', 'TOWER_HOST'])),
        controller_oauthtoken=dict(required=False, aliases=['tower_username'], fallback=(env_fallback, ['CONTROLLER_OAUTH_TOKEN', 'TOWER_OAUTH_TOKEN'])),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    inventories = __get_inventories(
        module.params.get('controller_host'), 
        module.params.get('controller_oauthtoken')
    )

    # Run the export process
    try:
        module.exit_json(changed=True, inventories=inventories)
    except Exception as e:
        module.fail_json(msg="Failed to export inventories {0}".format(e))

if __name__ == '__main__':
    main()