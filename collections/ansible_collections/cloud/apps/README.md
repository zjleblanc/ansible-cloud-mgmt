# cloud.apps

Ansible roles for deploying common applications on RHEL servers. This is a
local, in-repo collection (not published to Galaxy) used by playbooks under
[`playbooks/aws/`](../../../playbooks/aws/) — most notably
[`install_apps.yml`](../../../playbooks/aws/install_apps.yml).

## Supported platforms

- RHEL 9

All roles install packages from standard RHEL BaseOS / AppStream repositories
only — no EPEL or other third-party repositories are required.

## Roles

| Role | Description |
| --- | --- |
| [`kafka`](roles/kafka/README.md) | Install and configure Kafka / ZooKeeper |
| [`httpd`](roles/httpd/README.md) | Install and configure the Apache HTTP Server |
| [`cockpit`](roles/cockpit/README.md) | Install and enable the Cockpit web console |
| [`postgresql`](roles/postgresql/README.md) | Install and configure a PostgreSQL server |
| [`valkey`](roles/valkey/README.md) | Install and configure a Valkey server |

Each role documents its variables in both a `README.md` and a
`meta/argument_specs.yml` (viewable via `ansible-doc -t role cloud.apps.<role>`).

## Usage

Roles are referenced by their fully-qualified name (`cloud.apps.<role>`). The
[`install_apps.yml`](../../../playbooks/aws/install_apps.yml) playbook gates
each role behind membership in the `install_apps` list:

```yaml
---
- name: Install Applications
  hosts: "{{ _hosts | default('omit') }}"
  gather_facts: false
  become: true

  roles:
    - role: cloud.apps.kafka
      when: "'kafka' in install_apps"
      vars:
        kafka_mode: "{{ _kafka_mode | default('zookeeper') }}"

    - role: cloud.apps.httpd
      when: "'httpd' in install_apps"

    - role: cloud.apps.cockpit
      when: "'cockpit' in install_apps"

    - role: cloud.apps.postgresql
      when: "'postgresql' in install_apps"

    - role: cloud.apps.valkey
      when: "'valkey' in install_apps"
```

Run with, e.g., `install_apps: ["cockpit", "valkey"]`.

## Author Information

**Zach LeBlanc**

Red Hat
