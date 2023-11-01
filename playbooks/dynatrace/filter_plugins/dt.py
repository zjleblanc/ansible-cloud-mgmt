#!/usr/bin/python
from datetime import datetime, timedelta

class FilterModule(object):
    def filters(self):
        return {
            'codify': self.do_codify,
            'dt_problem_hosts': self.dt_problem_hosts
        }
    
    def do_codify(self, content, endline='\n'):
        return '[code]<pre>' + content.replace(endline,'<br>') + '</pre>[/code]'
    
    def dt_problem_hosts(self, problem):
        hosts = []
        evidence = problem.get('evidenceDetails', {})
        for detail in evidence.get('details', []):
            for prop in detail.get('data', {}).get('properties', []):
                if prop.get('key') == 'dt.entity.host':
                    hosts.append(prop.get('value'))
                    continue
        return hosts