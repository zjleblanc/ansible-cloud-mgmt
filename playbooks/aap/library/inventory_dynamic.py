#!/usr/bin/python
# coding: utf-8 -*-

# (c) 2017, Zachary LeBlanc <zleblanc@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule, env_fallback

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'], 'supported_by': 'community'}


DOCUMENTATION = '''
---
module: export
author: "Zachary LeBlanc (@zjleblanc)"
short_description: export dynamic inventories from Automation Platform Controller without dependent hosts/group configs.
description:
    - Export dynamic inventories from Automation Platform Controller.
options:
notes:
  - Specify list of names to isolate dynamic inventories from static inventories in your Ansible Automation Platform
  - Use the "ge_25" parameter when exporting from Ansible Automation Platform >=2.5
'''

EXAMPLES = '''
- name: Export dynamic inventory configurations
  register: r_get_all_inventories
  inventory_dynamic:
    ge_25: true # flag for AAP 2.5+
    names:
      - Service Now Inventory
      - Cloud Inventory
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

def __get_inventories(host, token, names, is_ge_25):
    resource = "/api/controller/v2/inventories/" if is_ge_25 else "/api/v2/inventories/"
    url = "https://" + host + resource
    res = requests.get(url, headers={"Authorization": "Bearer " + token})
    inventories_raw = res.json()['results']
    
    inventories_dynamic = []
    for inv in inventories_raw:
        if names and inv['name'] not in names:
            continue
        if inv['related'].get('instance_groups', None):
            inv['instance_groups'] = __get_related(host, token, inv['related']['instance_groups'])
        if inv['related'].get('input_inventories', None):
            inv['input_inventories'] = __get_related(host, token, inv['related']['input_inventories'])
        inventories_dynamic.append(inv)

    inventories = map(__map_to_cac, inventories_dynamic)
    return list(inventories)

def main():
    argument_spec = dict(
        controller_host=dict(required=False, aliases=['tower_host'], fallback=(env_fallback, ['CONTROLLER_HOST', 'TOWER_HOST'])),
        controller_oauthtoken=dict(required=False, no_log=True, aliases=['tower_username'], fallback=(env_fallback, ['CONTROLLER_OAUTH_TOKEN', 'TOWER_OAUTH_TOKEN'])),
        names=dict(required=False,type=list,default=None),
        ge_25=dict(required=False,type=bool,default=False)
    )

    module = AnsibleModule(argument_spec=argument_spec)

    inventories = __get_inventories(
        module.params.get('controller_host'), 
        module.params.get('controller_oauthtoken'),
        module.params.get('names'),
        module.params.get('ge_25'),
    )

    # Run the export process
    try:
        module.exit_json(changed=True, cac={"controller_inventories": inventories})
    except Exception as e:
        module.fail_json(msg="Failed to export inventories {0}".format(e))

if __name__ == '__main__':
    main()