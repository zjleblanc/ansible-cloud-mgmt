send_email
=========

Send an e-mail - defaults to using gmail and expects an app password to be provided.

Formerly named ``send-email``. Update any ``include_role`` / AAP references to ``send_email``.

Galaxy Tags: \[ email gmail \]

Role Variables
--------------

Canonical names use the ``send_email_`` prefix. Legacy ``email_smtp_*`` names still work.

| Variable | Default | Notes |
| -------- | ------- | ----- |
| send_email_smtp_server | smtp.gmail.com | legacy: email_smtp_server |
| send_email_smtp_server_port | 587 | legacy: email_smtp_server_port |
| send_email_smtp_from_address | ansible-zach@gmail.com | legacy: email_smtp_from_address |
| send_email_smtp_subject | Ansible Notification | legacy: email_smtp_subject |
| send_email_smtp_body | This is an ansible notification. | legacy: email_smtp_body |
| send_email_smtp_replyto_address | no-reply@gmail.com | legacy: email_smtp_replyto_address |
| send_email_smtp_subtype | plain | legacy: email_smtp_subtype |
| send_email_smtp_to_address | (required) | legacy: email_smtp_to_address |
| send_email_smtp_username | (required) | legacy: email_smtp_username |
| send_email_smtp_password | (required) | legacy: email_smtp_password |

License
-------

MIT

Author Information
-------
**Zach LeBlanc**

Red Hat
