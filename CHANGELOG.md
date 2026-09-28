# Changelog

All notable changes to this project will be documented in this file.

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
