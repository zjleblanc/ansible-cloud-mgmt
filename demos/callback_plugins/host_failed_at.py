# host_failed_at.py
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import datetime
import smtplib
from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ansible.plugins.callback import CallbackBase

DOCUMENTATION = '''
    callback: host_failed_at
    type: notification
    short_description: Records failed tasks with reason and timestamp, and emails the report
    version_added: "2.0"
    description:
      - Records the task name, failure reason, and timestamp for any host failures
      - Emails the failure report at the end of the playbook run
    requirements:
      - Set in callback_plugins directory and enabled via config
      - Environment variables for SMTP (or hardcoded settings)
'''

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'host_failed_at'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.failed_tasks = {}

    def v2_playbook_on_start(self, playbook):
        self.playbook_name = os.path.basename(playbook._file_name)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        task_name = result.task_name or result.task.get_name()
        timestamp = datetime.datetime.now().isoformat()
        reason = result._result.get('msg', 'No reason provided')

        self.failed_tasks[host] = {
            'task': task_name,
            'reason': reason,
            'timestamp': timestamp
        }

    def v2_playbook_on_stats(self, stats):

        # Build the report
        report = ""
        for host, info in self.failed_tasks.items():
            report += f"{host} failed at {info['timestamp']} on task: '{info['task']}'\n"
            report += f"  Reason: {info['reason']}\n\n"
            self._display.display(f"[host_failed_at] Host '{host}' failed at '{info['task']}' at {info['timestamp']}: {info['reason']}")

        if self.failed_tasks and os.getenv("SMTP_SERVER"):
            self._send_email(report)
        else:
          self._display.display(f"[host_failed_at] No SMTP configuration provided, skipping e-mail...")

    def _send_email(self, report_body):
        # Get SMTP settings from environment variables
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT"))
        smtp_user = os.getenv("SMTP_USER")
        smtp_password = os.getenv("SMTP_PASSWORD")
        email_from = os.getenv("SMTP_EMAIL_FROM")
        email_to = os.getenv("SMTP_EMAIL_TO")
        subject = f"Ansible Failure Report: Playbook [{self.playbook_name}]"

        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        with open(plugin_dir + '/host_failed_at_report.html.j2') as tmpl:
            template = Template(tmpl.read())
        
        html = template.render(playbook_name=self.playbook_name, failed_tasks=self.failed_tasks)

        msg = MIMEMultipart("alternative")
        msg.attach(MIMEText(html, 'html'))
        msg["Subject"] = subject
        msg["From"] = email_from
        msg["To"] = email_to

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(email_from, [email_to], msg.as_string())
            server.quit()
            self._display.display(f"[host_failed_at] Report emailed to {email_to}")
        except Exception as e:
            self._display.warning(f"[host_failed_at] Failed to send email: {e}")
