# Changelog

All notable changes to this project will be documented in this file.

## 2026-09-30 — Add rhel9_apps and rhel_apps target platforms for EC2 provisioning

### Added
- `rhel9_apps` and `rhel_apps` entries to `launch_templates` in `playbooks/aws/vars/create_ec2_infra.yml`, modeled on the `rhel_dev` template (RHEL9 and RHEL10 AMIs respectively), each carrying an `install_apps` list (`kafka`, `cockpit`, `postgresql`, `redis`).
- `lt_install_apps` variable in `create_ec2_infra.yml` that reads the new `install_apps` key from `launch_templates[target_platform]`, defaulting to `[]` for platforms without one.

### Changed
- `playbooks/aws/create_vm.yml`: `set_stats` now forwards `install_apps` (from `lt_install_apps`) so a chained `install_apps.yml` run knows which application roles to install for the provisioned platform.

## 2026-09-30 — Add local `cloud.apps` collection with httpd/cockpit/postgresql/redis roles

### Added
- Local `cloud.apps` collection at `collections/ansible_collections/cloud/apps/` (`galaxy.yml`, `README.md`, `CHANGELOG.md`, `meta/runtime.yml`) providing RHEL application roles referenced by FQCN (e.g. `cloud.apps.kafka`).
- `cloud.apps.httpd`, `cloud.apps.cockpit`, `cloud.apps.postgresql`, and `cloud.apps.redis` roles (defaults, tasks, handlers, templates where applicable, `meta/argument_specs.yml`, `README.md`), installing only from standard RHEL BaseOS/AppStream repos.
- `meta/argument_specs.yml` for every role in the collection, including `kafka`, documenting variable types, defaults, choices, and nested options.

### Changed
- Migrated the `kafka` role from `roles/kafka/` into `collections/ansible_collections/cloud/apps/roles/kafka/`; updated template `src:` paths and the role README accordingly.
- `playbooks/aws/install_apps.yml`: roles now referenced by FQCN (`cloud.apps.kafka`, `cloud.apps.httpd`, `cloud.apps.cockpit`, `cloud.apps.postgresql`, `cloud.apps.redis`), each gated on the `install_apps` list variable.
- `README.md`: updated the repository layout and roles tables to reflect the local `cloud.apps` collection.
- `demos/docs/eda_kafka_sandbox.md`: updated the kafka role link to its new collection path.

### Removed
- `roles/kafka/` (superseded by `collections/ansible_collections/cloud/apps/roles/kafka/`).

## 2026-09-30 — Add restart-service and reboot-machine playbooks with SC Task tracking

### Added
- `playbooks/aws/restart_service.yml` playbook to restart a named service (`service_name`) on an EC2 instance identified by `_host`, supporting RHEL (`ansible.builtin.systemd`) and Windows (`ansible.windows.win_service`), with post-restart verification that the service is active/running.
- `playbooks/aws/reboot_machine.yml` playbook to reboot an EC2 instance identified by `_host`, supporting RHEL (`ansible.builtin.reboot`) and Windows (`ansible.windows.win_reboot`), which handle disconnection, wait for the reboot to complete, and confirm reconnection before reporting status.
- Both new playbooks follow the `resize_disk.yml` pattern: input validation, ServiceNow SC Task lifecycle tracking (linked to a RITM and its parent REQ, skipped with a warning when `ritm_number` is not supplied), platform detection via `hostvars`/EC2 instance info, and closing the SC Task with work notes on completion.

### Changed
- `README.md`: added `reboot_machine.yml` and `restart_service.yml` entries to the AWS playbooks table.

## 2026-09-29 — Fix disk resize target/growth calculation in resize_disk.yml

### Fixed
- `playbooks/aws/resize_disk.yml`: fixed the growth-vs-target volume size calculation, which could silently resolve to `0 GiB` (or raise a templating type error) depending on the execution environment's Ansible-core/Jinja version. `requested_size_gib` is now explicitly cast with `| float` at every arithmetic use site instead of relying on the templar to preserve native numeric types across `set_fact`/`vars` boundaries.
- Added defensive `| float` casts to the `disk_growth`/`disk_target` sentinel comparisons in the input validation assert and the growth/target selection `ternary()` conditions, so string-typed extra vars (e.g. from CLI `-e` or text-type survey fields) no longer break the comparison.

## 2026-09-28 — Point ansible-navigator at the personal ee-default image

### Changed
- Updated `ansible-navigator.yml` execution-environment image from `automation-hub.autodotes.com/ee-default:d7393656` to `quay.io/zleblanc/ee-default:latest`.

## 2026-09-28 — Add dynamic disk resize playbook with SC Task tracking

### Added
- `playbooks/aws/resize_disk.yml` playbook to resize EC2 EBS volumes based on either a relative growth amount (`disk_growth`) or an absolute target size (`disk_target`), with `disk_unit` of `GB`/`MB`/`TB`, without modifying the existing `add_disk_space.yml`.
- `playbooks/aws/tasks/resize_vol_rhel_dynamic.yml` and `playbooks/aws/tasks/resize_vol_windows_dynamic.yml` task files that apply the calculated volume size per platform.
- `playbooks/aws/tasks/capture_df_results_sc_task.yml` task file to record pre/post-remediation `df` output as ServiceNow SC Task work notes.
- ServiceNow SC Task lifecycle tracking (linked to a RITM and its parent REQ) for this workflow, including a skip warning when `ritm_number` is not supplied.

## 2026-08-18 — Initialize changelog and recent repository updates

### Added
- `jira_assets` dynamic inventory plugin and configuration to support Jira Assets (CMDB) as an inventory source.
- `AGENTS.md` containing mandatory quality gates, linting profiles, and contributor guidance.
- Dynamic inventory documentation section to `README.md`.

### Changed
- Updated ServiceNow playbooks (`patch_vm.yml`, `create_cr_from_tmpl.yml`, `create_incident.yml`) to use `SN_USERNAME` environment lookup instead of hardcoded usernames.
- Refined `pre-commit` configuration for `ansible-lint` to trigger only on Ansible-related paths while maintaining full-project linting scope.
- Expanded `README.md` with comprehensive repository layout, playbook catalogs, and tooling information.

### Fixed
- Addressed project-wide `ansible-lint` warnings and errors.
- Configured `ansible-lint` to use `extra_vars` for `_host` and `_hosts` to satisfy syntax-check for AAP-driven playbooks.
