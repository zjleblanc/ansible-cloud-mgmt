# azure snapshot mgmt

This directory contains playbooks to demonstrate managing disks, and their respective snapshots, in Azure.

### objectives:
- create disks with tags
- snapshot disks
- scan for snapshots based on retention status (determined by tags)
- email snapshot owners if snapshots are past retention
- delete snapshots based on retention status

### playbook execution order
- [create_disks.yml](./create_disks.yml)
- [snapshot_disks.yml](./snapshot_disks.yml)
- [scan_snapshots.yml](./scan_snapshots.yml)
- [delete_snapshots.yml](./delete_snapshots.yml)

### filter plugins
| name | purpose |
| --- | --- |
| date_offset | get a date based on an offset, useful for simulating scans in the past/future |
| past_retention | filters list of snapshots based on retention status using resource tags |

### accessory playbooks
- [tag_disks.yml](./tag_disks.yml)
- [tag_snapshots.yml](./tag_snapshots.yml)
- [get_disks.yml](./get_disks.yml)