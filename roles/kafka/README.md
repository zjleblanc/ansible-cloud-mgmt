kafka
=========

Install a kafka instance on linux, configuring zookeeper with an internal and external listener.

_Tested on Amazon EC2, RHEL 9.3_

Requirements
------------

Linux server with capacity for running lightweight kafka cluster. 

_Tested on t2.medium EC2 instance_

Role Variables
--------------

```yaml
kafka_version: "3.7.0" # Specify your desired Kafka version
scala_version: "2.13"  # Specify the Scala version compatible with your Kafka version
kafka_install_dir: "/opt/kafka"
kafka_data_dir: "/var/lib/kafka"
zookeeper_data_dir: "/var/lib/zookeeper" # For internal Zookeeper or KRaft
java_home: "/usr/lib/jvm/jre-11-openjdk" # Adjust based on your Java installation
```

Example Playbook
----------------

```yaml
---
- name: Install Applications
  hosts: "{{ _hosts | default('omit') }}"
  gather_facts: false
  become: true

  pre_tasks:
    - name: Wait for connection (3m)
      ansible.builtin.wait_for_connection:
        timeout: 180

    - name: Gather facts
      ansible.builtin.setup:

  roles:
    - name: kafka
      when: "'kafka' in install_apps"
      vars:
        kafka_mode: "{{ _kafka_mode | default('zookeeper') }}"

```

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zach LeBlanc**

Red Hat
