cloud.apps.valkey
=========

Install and configure a Valkey server on RHEL.

_Tested on RHEL 9_

Requirements
------------

RHEL server with `valkey` available from the AppStream repository (no
EPEL or third-party repos required).

Role Variables
--------------

See [`meta/argument_specs.yml`](meta/argument_specs.yml) for the full,
validated specification (types, defaults, choices). Summary:

```yaml
valkey_bind: "127.0.0.1"
valkey_port: 6379
valkey_maxmemory: "256mb"
valkey_maxmemory_policy: "noeviction"  # noeviction | allkeys-lru | volatile-lru | allkeys-random | volatile-random | volatile-ttl
valkey_manage_firewall: true
```

Example Playbook
----------------

```yaml
---
- name: Install Applications
  hosts: "{{ _hosts | default('omit') }}"
  gather_facts: false
  become: true

  roles:
    - role: cloud.apps.valkey
      when: "'valkey' in install_apps"
```

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zach LeBlanc**

Red Hat
