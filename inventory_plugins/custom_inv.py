import os
from typing import Any
from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

INV = {
    "group001": {
        "hosts": ["host001", "host002"],
        "vars": {
                "testvar": "testvalue",
                "testenv": os.getenv("ENV_VAR_FROM_CREDENTIAL")
        },
        "children": ["group002"]
    },
    "group002": {
        "hosts": ["host003", "host004"],
        "vars": {
            "var2": 500
        },
        "children":[]
    }
}

class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

    NAME = 'custom_inv'

    def __init__(self):
        super(InventoryModule, self).__init__()
        self.address = None
        self.plugin = None

    def verify_file(self, path: str):
        if super(InventoryModule, self).verify_file(path):
            return path.endswith('yaml') or path.endswith('yml')
        return False

    def parse(self, inventory: Any, loader: Any, path: Any, cache: bool = True) -> Any:
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)  # This also loads the cache
        try:
            for group in INV.keys():
                self.inventory.add_group(group)
                for host in INV[group].get("hosts", []):
                    self.inventory.add_host(host, group=group)
                for child in INV[group].get("children", []):
                    self.inventory.add_group(child)
                for k,v in INV[group].get('vars', {}).items():
                    self.inventory.set_variable(group, k, v)
        except Exception as e:
            raise AnsibleParserError(f'Failed to parse inventory file {e}', e)
