# Changelog

All notable changes to this project will be documented in this file.

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
