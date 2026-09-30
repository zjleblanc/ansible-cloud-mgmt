cloud.apps.httpd
=========

Install and configure the Apache HTTP Server (httpd) on RHEL.

_Tested on RHEL 9_

Requirements
------------

RHEL server with `httpd` and `mod_ssl` available from the BaseOS
repository (no EPEL or third-party repos required).

Role Variables
--------------

See [`meta/argument_specs.yml`](meta/argument_specs.yml) for the full,
validated specification (types, defaults). Summary:

```yaml
httpd_listen_port: 80
httpd_document_root: "/var/www/html"
httpd_server_name: "{{ ansible_fqdn }}"
httpd_enable_ssl: true
httpd_manage_firewall: true
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
    - role: cloud.apps.httpd
      when: "'httpd' in install_apps"
```

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zach LeBlanc**

Red Hat
