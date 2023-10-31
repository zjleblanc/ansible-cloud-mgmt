#!/usr/bin/python
from datetime import datetime, timedelta

class FilterModule(object):
    def filters(self):
        return {
            'dt_problem_hosts': self.dt_problem_hosts,
        }
    
    def dt_problem_hosts(self, problem):
        hosts = []
        evidence = problem.get('evidenceDetails', {})
        for detail in evidence.get('details', []):
            for prop in detail.get('data', {}).get('properties', []):
                if prop.get('key') == 'dt.entity.host':
                    hosts.append(prop.get('value'))
                    continue
        return hosts