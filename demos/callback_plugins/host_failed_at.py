# host_failed_at.py
from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
from ansible.plugins.callback import CallbackBase

DOCUMENTATION = '''
    callback: host_failed_at
    type: notification
    short_description: Records the task name each host failed on
    version_added: "2.0"
    description:
      - This callback records the task name where each host fails during execution.
    requirements:
      - Set in callback_plugins directory and enabled via config
'''

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'host_failed_at'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.failed_tasks = {}

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        task_name = result.task_name or result.task.get_name()
        self.failed_tasks[host] = task_name

    def v2_playbook_on_stats(self, stats):
        for host, task in self.failed_tasks.items():
            self._display.display(f"{host} failed at: {task}")
