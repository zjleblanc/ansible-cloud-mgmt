# Backing up the Platform

For any application, especially something as critical as Ansible Automation Platform (AAP), customers often need to have a backup process in place. The traditional, vm-based installer (setup.sh) for AAP also handles the backup process which can be scheduled to run by various mechanisms (same applies for bare-metal). Since we have AAP, why not Ansible? I finally got around to writing and scheduling my backups which includes an upload to S3 for storage purposes. In the future, the container-based installer backup process might look a bit different, but the workflow should still apply.

[The Playbook](../backup_platform.yml)

## The Process

1. Cleanup old backups (optional)
2. Create a backup directory
3. Run the setup script
4. Locate backup file using "latest" symlink
5. Upload to S3 (optional)

## Variables

| Name | Default | Description |
| --- | --- | --- |
| ansible_installation_dir | **_Required_** | Location the installer was unzipped (directory containing setup.sh) |
| ansible_backups_dir | **_Required_** | Location to put the resulting backup (this can be large) |
| aws_region | us-east-2 | AWS region with target S3 |
| aws_s3_bucket | autodotes-app-backups | Name of S3 bucket |
| 🚩 cleanup_backups_dir | true | Delete existing backups in specified destination |
| 🚩 skip_backup | false | Skip the backup step (useful when upload fails but backup was successful) |
| 🚩 upload_backup_to_s3 | true | Upload to backup to S3 |