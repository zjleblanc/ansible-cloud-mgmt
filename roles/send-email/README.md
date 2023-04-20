send-email
=========

Send an e-mail - defauls to using gmail and expects an app password to be provided.

Galaxy Tags: \[ email gmail \]

Role Variables
--------------

| Variable | Default | Value or Expression |
| -------- | ------- | ------------------- |
| email_smtp_server | ✅ | smtp.gmail.com |
| email_smtp_server_port | ✅ | 587 |
| email_smtp_from_address | ✅ | ansible-zach@gmail.com |
| email_smtp_subject | ✅ | Ansible Notification |
| email_smtp_body | ✅ | This is an ansible notification. |
| email_smtp_replyto_address | ✅ | no-reply@gmail.com |
| email_smtp_subtype | ✅ | plain |
| email_smtp_to_address | ❌ | |
| email_smtp_username | ❌ | |
| email_smtp_password | ❌ | |

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zach LeBlanc**

Red Hat
