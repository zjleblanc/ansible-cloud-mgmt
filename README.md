# ansible-cloud-mgmt

Ansible playbooks, demos, roles, and supporting tooling for cloud and platform management across AWS, Azure, GCP, VMware, ServiceNow, HashiCorp Vault, and Ansible Automation Platform (AAP).

## Repository layout

| Path | Purpose |
| --- | --- |
| `playbooks/` | Production-oriented and reusable playbooks by domain |
| `demos/` | Example / sandbox playbooks and plugins |
| `roles/` | Shared Ansible roles (`kafka`, `send_email`) |
| `inventories/` | Inventory sources (dynamic and static) |
| `collections/` | Collection requirements for project sync (AAP) |
| `tests/` | Lint-only collection requirements for `ansible-lint` |
| `scripts/` | Helper scripts (Postman conversion, CVE reporting, etc.) |
| `assets/` | API Postman collections and related assets |
| `filter_plugins/` | Shared Jinja filters |
| `inventory_plugins/` | Custom inventory plugins |

## Tooling

Quality and secret scanning are enforced with [pre-commit](https://pre-commit.com):

```bash
pre-commit install
pre-commit run --all-files
```

| Tool | Config | Role |
| --- | --- | --- |
| [ansible-lint](https://ansible.readthedocs.io/projects/lint/) (`v26.4.0`) | `.ansible-lint` | Production-profile lint of Ansible content |
| [gitleaks](https://github.com/gitleaks/gitleaks) (`v8.30.0`) | `.pre-commit-config.yaml` | Detect secrets before commit |

See [AGENTS.md](./AGENTS.md) for contributor and AI-agent conventions.

---

## Playbooks

Top-level entry playbooks (task/vars includes under each domain are omitted).

### Ansible Automation Platform (`playbooks/aap/`)

| Playbook | Description |
| --- | --- |
| [`ah_update_local_user_pw.yml`](playbooks/aap/ah_update_local_user_pw.yml) | Update password for an Automation Hub local user |
| [`backup_platform.yml`](playbooks/aap/backup_platform.yml) | Backup Ansible Automation Platform |
| [`create_label.yml`](playbooks/aap/create_label.yml) | Create a Controller label |
| [`export_dynamic_inventory.yml`](playbooks/aap/export_dynamic_inventory.yml) | Export dynamic inventory (without hosts and groups) |
| [`export_inventory.yml`](playbooks/aap/export_inventory.yml) | Export dynamic inventory |
| [`pah_sync_repositories.yml`](playbooks/aap/pah_sync_repositories.yml) | Sync Automation Hub repositories |
| [`query_job_events.yml`](playbooks/aap/query_job_events.yml) | Query job events |
| [`refresh_rh_token.yml`](playbooks/aap/refresh_rh_token.yml) | Refresh Red Hat Automation Hub token |
| [`test_lookup_plugin.yml`](playbooks/aap/test_lookup_plugin.yml) | Test credential lookup plugin(s) |

### AWS (`playbooks/aws/`)

| Playbook | Description |
| --- | --- |
| [`add_disk_space.yml`](playbooks/aws/add_disk_space.yml) | Expand disk space on an EC2 instance |
| [`create_vm.yml`](playbooks/aws/create_vm.yml) | Create EC2 instances |
| [`delete_vm.yml`](playbooks/aws/delete_vm.yml) | Terminate EC2 instances |
| [`ec2_process_report.yml`](playbooks/aws/ec2_process_report.yml) | Process an EC2 report against inventory |
| [`gather_facts.yml`](playbooks/aws/gather_facts.yml) | Demo playbook for ansible-navigator |
| [`install_agents.yml`](playbooks/aws/install_agents.yml) | Install monitoring/agent packages on hosts |
| [`install_apps.yml`](playbooks/aws/install_apps.yml) | Install applications on hosts |
| [`patch_vm.yml`](playbooks/aws/patch_vm.yml) | Patch EC2 instances (Linux/Windows) |
| [`pb_ai_rca.yml`](playbooks/aws/pb_ai_rca.yml) | Generate AI root-cause analysis for an incident |
| [`restore_from_snapshot.yml`](playbooks/aws/restore_from_snapshot.yml) | Restore an EC2 volume from snapshot |
| [`snapshot_vm.yml`](playbooks/aws/snapshot_vm.yml) | Snapshot EC2 volumes |

### Azure (`playbooks/azure/`)

| Playbook | Description |
| --- | --- |
| [`custom_script_ext.yml`](playbooks/azure/custom_script_ext.yml) | Run CustomScript extension on an Azure VM |
| [`read_kv_secret.yml`](playbooks/azure/read_kv_secret.yml) | Read a secret from Azure Key Vault |

#### Snapshot management (`playbooks/azure/snapshot_mgmt/`)

See the [snapshot_mgmt README](playbooks/azure/snapshot_mgmt/README.md) for execution order and filter plugins.

| Playbook | Description |
| --- | --- |
| [`create_disks.yml`](playbooks/azure/snapshot_mgmt/create_disks.yml) | Create managed disks |
| [`get_disks.yml`](playbooks/azure/snapshot_mgmt/get_disks.yml) | List managed disks |
| [`snapshot_disks.yml`](playbooks/azure/snapshot_mgmt/snapshot_disks.yml) | Snapshot managed disks |
| [`scan_snapshots.yml`](playbooks/azure/snapshot_mgmt/scan_snapshots.yml) | Scan snapshots (retention / ownership) |
| [`delete_snapshots.yml`](playbooks/azure/snapshot_mgmt/delete_snapshots.yml) | Delete snapshots past retention |
| [`tag_disks.yml`](playbooks/azure/snapshot_mgmt/tag_disks.yml) | Tag managed disks |
| [`tag_snapshots.yml`](playbooks/azure/snapshot_mgmt/tag_snapshots.yml) | Tag snapshots |

### GCP (`playbooks/gcp/`)

| Playbook | Description |
| --- | --- |
| [`gcloud_cli_test.yml`](playbooks/gcp/gcloud_cli_test.yml) | Test gcloud CLI auth via AAP credential |
| [`gcp_convert_license.yml`](playbooks/gcp/gcp_convert_license.yml) | Convert RHEL VM licenses in a GCP project |

### VMware (`playbooks/vmware/`)

| Playbook | Description |
| --- | --- |
| [`deploy.yml`](playbooks/vmware/deploy.yml) | Provision a VMware guest |
| [`info.yml`](playbooks/vmware/info.yml) | Gather VMware guest info |
| [`no_op.yml`](playbooks/vmware/no_op.yml) | Gather facts about a VMware guest (no-op style) |
| [`power.yml`](playbooks/vmware/power.yml) | Manage VMware guest power state |
| [`snapshot.yml`](playbooks/vmware/snapshot.yml) | Manage VMware guest snapshots |

### ServiceNow (`playbooks/snow/`)

| Playbook | Description |
| --- | --- |
| [`create_cr_from_tmpl.yml`](playbooks/snow/create_cr_from_tmpl.yml) | Create a change request from a template |
| [`create_incident.yml`](playbooks/snow/create_incident.yml) | Create a ServiceNow incident |
| [`manage_ci.yml`](playbooks/snow/manage_ci.yml) | Manage configuration items |
| [`manage_cr.yml`](playbooks/snow/manage_cr.yml) | Manage change requests |
| [`manage_resource.yml`](playbooks/snow/manage_resource.yml) | Manage ServiceNow resources |
| [`populate_cmdb_ec2.yml`](playbooks/snow/populate_cmdb_ec2.yml) | Populate CMDB from EC2 instances |
| [`update_incident.yml`](playbooks/snow/update_incident.yml) | Update a ServiceNow incident |

### HashiCorp Vault (`playbooks/vault/`)

| Playbook | Description |
| --- | --- |
| [`install_vault.yml`](playbooks/vault/install_vault.yml) | Install Community Vault (RPM or Podman) |

### DNS, Citrix, APIs, misc.

| Playbook | Description |
| --- | --- |
| [`dns/dynamic_dns.yml`](playbooks/dns/dynamic_dns.yml) | Dynamic DNS updates |
| [`citrix/provision_vdi.yml`](playbooks/citrix/provision_vdi.yml) | Example: provision a Citrix DaaS VDI via URI |
| [`apis/spotify_uri.yml`](playbooks/apis/spotify_uri.yml) | Interact with Spotify API using `uri` |
| [`apis/tmdb_uri.yml`](playbooks/apis/tmdb_uri.yml) | Manage a TMDB account with `uri` |
| [`no_op.yml`](playbooks/no_op.yml) | No-op playbook for demos / connectivity checks |

---

## Demos

Example and sandbox content under `demos/`.

| Playbook | Description |
| --- | --- |
| [`aws_to_snow_cmdb.yml`](demos/aws_to_snow_cmdb.yml) | Gather AWS inventory and sync into ServiceNow CMDB |
| [`cyberark_per_host.yml`](demos/cyberark_per_host.yml) | CyberArk per-host password demo |
| [`failed_at_report.yml`](demos/failed_at_report.yml) | Demo failing tasks with custom failure reporting callback |
| [`in_memory_inv_test.yml`](demos/in_memory_inv_test.yml) | Create and automate an in-memory host |
| [`selenium_automation_dashboard.yml`](demos/selenium_automation_dashboard.yml) | Confirm Automation Dashboard status via Selenium screenshot |
| [`selenium_screen_capture.yml`](demos/selenium_screen_capture.yml) | Take a screenshot with Selenium |
| [`sn_create_tables.yml`](demos/sn_create_tables.yml) | Create ServiceNow tables and custom fields |
| [`vault_per_host.yml`](demos/vault_per_host.yml) | HashiCorp Vault per-host password demo |

Supporting demo assets (not standalone entry playbooks):

- `demos/aws_data.yml` — sample AWS instance data
- `demos/vars/` — demo variables (including vaulted secrets; do not commit plaintext)
- `demos/tasks/` — shared task includes for CMDB / table demos
- `demos/callback_plugins/` — custom failure-at reporting callbacks
- `demos/filter_plugins/` — AWS→ServiceNow object filters
- `demos/scripts/` — Selenium helpers

---

## Inventories

| Path | Plugin | Description |
| --- | --- | --- |
| [`inventories/aws/`](inventories/aws/) | `amazon.aws.aws_ec2` | EC2 dynamic inventory |
| [`inventories/custom.yaml`](inventories/custom.yaml) | `custom_inv` | Sample custom inventory plugin |
| [`inventories/jira_assets/`](inventories/jira_assets/) | `jira_assets` | Jira Assets (CMDB) dynamic inventory via AQL |
| [`inventories/snow/`](inventories/snow/) | `servicenow.itsm.now` | ServiceNow CMDB dynamic inventory |
| [`inventories/vmware/`](inventories/vmware/) | `community.vmware.vmware_vm_inventory` | VMware VM dynamic inventory |

Custom inventory plugins live under [`inventory_plugins/`](inventory_plugins/).

## Roles

| Role | Description |
| --- | --- |
| [`kafka`](roles/kafka/) | Install and configure Kafka / ZooKeeper |
| [`send_email`](roles/send_email/) | Send email notifications |

## Running playbooks

Local runs typically use [ansible-navigator](https://ansible.readthedocs.io/projects/ansible-navigator/) with [`ansible-navigator.yml`](./ansible-navigator.yml) (execution environment + credential env passthrough). Many playbooks expect AAP extra vars such as `_host` / `_hosts` at runtime.
