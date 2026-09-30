cloud.apps.redis
=========

Install and configure a Redis server on RHEL.

_Tested on RHEL 9_

Requirements
------------

RHEL server with `redis` available from the AppStream repository (no
EPEL or third-party repos required).

Role Variables
--------------

See [`meta/argument_specs.yml`](meta/argument_specs.yml) for the full,
validated specification (types, defaults, choices). Summary:

```yaml
redis_bind: "127.0.0.1"
redis_port: 6379
redis_maxmemory: "256mb"
redis_maxmemory_policy: "noeviction"  # noeviction | allkeys-lru | volatile-lru | allkeys-random | volatile-random | volatile-ttl
redis_manage_firewall: true
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
    - role: cloud.apps.redis
      when: "'redis' in install_apps"
```

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zach LeBlanc**

Red Hat
