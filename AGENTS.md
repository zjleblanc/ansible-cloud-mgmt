# AGENTS.md

Guidance for humans and AI agents contributing to this repository. Prefer matching existing playbook style over inventing new patterns.

## Project purpose

Ansible content for cloud and platform management (AWS, Azure, GCP, VMware, ServiceNow, Vault, AAP). Changes should stay focused on playbooks, roles, demos, inventories, and related automation helpers.

## Mandatory quality gates

All commits are expected to pass **pre-commit** hooks defined in [`.pre-commit-config.yaml`](./.pre-commit-config.yaml).

```bash
pre-commit install
pre-commit run --all-files
```

| Hook | Tool | Expectation |
| --- | --- | --- |
| `ansible-lint` | ansible-lint `v26.4.0` + `ansible-core>=2.19.0` | Lint **all** Ansible content (hook always runs; does not rely on staged filenames) |
| `gitleaks` | gitleaks `v8.30.0` | No secrets, tokens, private keys, or credential material in the diff |

Do not skip hooks (`--no-verify`) unless the user explicitly requests it. Fix lint and secret findings instead.

### ansible-lint

Config: [`.ansible-lint`](./.ansible-lint)

- **Profile:** `production` — treat violations as blockers, not suggestions.
- **Kinds:** task/vars/handlers/meta paths are classified before playbook heuristics (important for files under `playbooks/` and `demos/`).
- **Extra vars for syntax-check:** `_host` and `_hosts` default to `localhost` so playbooks that parameterize hosts still parse offline.
- **Excluded from lint:** `.cache/`, `.venv/`, `vaulted/`, `archive/`, and vault ciphertext such as `demos/vars/secrets.yml`.
- **Collections for lint:** install/resolve from [`tests/requirements.yml`](./tests/requirements.yml) only. Do **not** add lint-only collections to [`collections/requirements.yml`](./collections/requirements.yml) (that file is used for AAP project sync).

When editing Ansible YAML:

- Keep FQCN module names where the repo already uses them.
- Name plays and tasks clearly; avoid unnamed tasks.
- Prefer `hosts: "{{ _host }}"` / `"{{ _hosts | default('omit') }}"` patterns already used for AAP-driven runs.
- Do not weaken lint by expanding `exclude_paths` or disabling rules unless there is a documented, unavoidable reason.

### gitleaks / secrets

- Never commit credentials, API keys, vault tokens, private keys, or plaintext secrets.
- Vaulted / ciphertext files may exist (e.g. under `demos/vars/`); do not “fix” them into plaintext for readability.
- Keep secrets out of docs, commit messages, and example variable values.
- Prefer Ansible Vault, AAP credentials, or external secret stores over embedding values in playbooks.

## File and naming conventions

| Area | Convention |
| --- | --- |
| Role directories | Snake_case (`send_email`, not `send-email`) |
| Playbooks | Snake_case YAML under domain folders (`playbooks/<domain>/`) |
| Task includes | `tasks/*.yml` next to the consuming playbooks |
| Demos | Self-contained examples under `demos/`; may include plugins/scripts |
| Docs | Prefer updating existing README sections; avoid unsolicited markdown |

## Editing guidance

- Match indentation, naming, and module usage of neighboring playbooks.
- Prefer small, focused diffs; do not refactor unrelated playbooks in the same change.
- Shared reusable logic belongs in `roles/` or `tasks/` includes, not copy-pasted across domains.
- Runtime-only vars for AAP (`_host`, `_hosts`, credentials) should remain parameters — do not hardcode environment-specific hosts.
- Filter/callback/inventory plugins should stay next to the content that needs them unless clearly shared (`filter_plugins/`, `inventory_plugins/`).

## Verification checklist (before finishing a change)

1. Run `pre-commit run --all-files` (or at least the hooks relevant to touched files).
2. Confirm ansible-lint is clean under the `production` profile.
3. Confirm gitleaks reports no findings.
4. If playbooks need new collections for lint/syntax, add them to `tests/requirements.yml` — not `collections/requirements.yml` — unless AAP sync must also install them.
5. Update [README.md](./README.md) playbook/demo directory entries when adding or removing top-level playbooks.

## Out of scope for agents

- Do not commit unless the user asks.
- Do not force-push, amend shared history, or disable hooks without explicit instruction.
- Do not invent new top-level tooling configs that duplicate pre-commit / ansible-lint without need.
