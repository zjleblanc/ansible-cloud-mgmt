# Selenium - Automation Dashboard

Many IT organizations are required to provide screen captures to satisfy audit and compliance policies that support change management. These tasks are tedious and often time-consuming, so I set out on a mission to see if I could build an execution environment with the appropriate tools to automate these efforts and provide adequate evidence. To make it interesting, I created a scenario where I will take down the newly released (tech preview) Automation Dashboard, remediate the issue, and attach evidence of the fix to a Service Now incident.

## Source Code

| Link | Purpose |
| --- | --- |
| [Playbook](../selenium_automation_dashboard.yml) | the ansible playbook which integrates with Service Now and invokes Selenium |
| [Python Script](../scripts/selenium_automation_dashboard.py) | the python script which interacts with Automation Dashboard and takes a screenshot |

## Execution Environment

The image I use in this demonstration is publicly available:<br>
`podman pull quay.io/zleblanc/ee-selenium:v4`


### Definition

```yaml
# https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json
---
version: 3

build_arg_defaults:
  ANSIBLE_GALAXY_CLI_COLLECTION_OPTS: '--pre'

dependencies:
  galaxy:
    collections:
      - name: servicenow.itsm
        version: 2.9.3
      - name: community.general
        version: 10.6.0
  python:
    - selenium
    - jmespath
  system:
    - pkgconf-pkg-config [platform:rpm]
    - systemd-devel [platform:rpm]
    - gcc [platform:rpm]
    - python3.11-devel [platform:rpm]
  ansible_core:
    package_pip: ansible-core
  ansible_runner:
    package_pip: ansible-runner

images:
  base_image:
    name: registry.redhat.io/ansible-automation-platform-25/ee-minimal-rhel8:latest

# Custom package manager path for the RHEL based images
options:
 package_manager_path: /usr/bin/microdnf

additional_build_files:
    - src: ../files/ansible.cfg
      dest: configs
    - src: ../files/google-chrome.repo
      dest: configs

additional_build_steps:
  prepend_galaxy:
    - COPY _build/configs/ansible.cfg /etc/ansible/ansible.cfg
  prepend_base:
    - COPY _build/configs/google-chrome.repo /etc/yum.repos.d/google-chrome.repo
    - RUN $PKGMGR -y install google-chrome-stable
  prepend_final:
    - >
      RUN $PKGMGR install -y unzip jq &&
      DRIVER=$(curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json | jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url') &&
      curl -o /tmp/chromedriver-linux64.zip $DRIVER &&
      unzip -j /tmp/chromedriver-linux64.zip -d /tmp/chromedriver && 
      cp /tmp/chromedriver/chromedriver /usr/local/bin/chromedriver &&
      $PKGMGR remove -y unzip jq 
  append_final:
    # Verify installed packages have compatible dependencies
    # Logged issue https://github.com/ansible/ansible-builder/issues/416
    - RUN pip3 check
    # Clean up
    - >
      RUN $PKGMGR update -y &&
      $PKGMGR clean all &&
      rm -rf /var/cache/{dnf,yum} &&
      rm -rf /var/lib/dnf/history.* &&
      rm -rf /var/log/*
```

### files/ansible.cfg

```
[galaxy]
server_list = certified, release_galaxy

[galaxy_server.certified]
url=https://console.redhat.com/api/automation-hub/content/published/
auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
token=REPLACE_WITH_YOUR_TOKEN

[galaxy_server.release_galaxy]
url=https://galaxy.ansible.com/
```

### files/google-chrome.repo

```
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
```