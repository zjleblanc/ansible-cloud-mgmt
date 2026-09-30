cloud.apps.cockpit
=========

Install and enable the Cockpit web console on RHEL.

_Tested on RHEL 9_

Requirements
------------

RHEL server with `cockpit` and `cockpit-ws` available from the BaseOS
repository (no EPEL or third-party repos required).

Role Variables
--------------

See [`meta/argument_specs.yml`](meta/argument_specs.yml) for the full,
validated specification (types, defaults). Summary:

```yaml
cockpit_packages:
  - cockpit
  - cockpit-ws
cockpit_manage_firewall: true
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
    - role: cloud.apps.cockpit
      when: "'cockpit' in install_apps"
```

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zach LeBlanc**

Red Hat
