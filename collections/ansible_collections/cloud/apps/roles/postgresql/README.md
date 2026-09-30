cloud.apps.postgresql
=========

Install and configure a PostgreSQL server on RHEL.

_Tested on RHEL 9_

Requirements
------------

RHEL server with `postgresql-server` and `postgresql` available from the
AppStream repository (no EPEL or third-party repos required).

Role Variables
--------------

See [`meta/argument_specs.yml`](meta/argument_specs.yml) for the full,
validated specification (types, defaults, nested options). Summary:

```yaml
postgresql_listen_addresses: "localhost"
postgresql_port: 5432
postgresql_data_dir: "/var/lib/pgsql/data"
postgresql_hba_entries:
  - type: local
    database: all
    user: all
    method: peer
  - type: host
    database: all
    user: all
    address: "127.0.0.1/32"
    method: scram-sha-256
  - type: host
    database: all
    user: all
    address: "::1/128"
    method: scram-sha-256
postgresql_manage_firewall: true
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
    - role: cloud.apps.postgresql
      when: "'postgresql' in install_apps"
```

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zach LeBlanc**

Red Hat
