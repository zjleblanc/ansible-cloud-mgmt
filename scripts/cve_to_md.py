import sys
import requests
import json

cves = []
with open(sys.argv[1], 'r', encoding='UTF-8') as file:
  while line := file.readline():
    cves.append(line.rstrip())

cve_data = {}
for cve in cves:
  resp = requests.get(f'https://access.redhat.com/hydra/rest/securitydata/cve/{cve}.json')
  if resp.status_code != 200:
    continue
  data = resp.json()
  severity = data.get('threat_severity', 'unk')
  if severity not in cve_data:
    cve_data[severity] = []
  cve_data[severity].append({
    "name": data['name'],
    "date": data['public_date'][:10],
    "bugzilla": data['bugzilla']['description'].replace('\n', ' '),
    "statement": data.get('statement', '').replace('\n', ' ')
  })

with open('data/cves.md', 'w') as outfile:
  outfile.write('# Red Hat CVE Metadata\n\n')
  outfile.write('| CVE | Date | Severity | Bugzilla Description | Statement |\n')
  outfile.write('| --- | --- | --- | :-- | :-- |\n')
  for cve in cve_data.get('Important', []):
    outfile.write(f"| [{cve['name']}](https://access.redhat.com/security/cve/{cve['name']}) | {cve['date']} | <span color='#a60000'>Important</span> | {cve['bugzilla']} | {cve['statement']} |\n")
  for cve in cve_data.get('Moderate', []):
    outfile.write(f"| [{cve['name']}](https://access.redhat.com/security/cve/{cve['name']}) | {cve['date']} | <span color='#9e4a06'>Moderate</span> | {cve['bugzilla']} | {cve['statement']} |\n")
  for cve in cve_data.get('Low', []):
    outfile.write(f"| [{cve['name']}](https://access.redhat.com/security/cve/{cve['name']}) | {cve['date']} | <span color='#96640f'>Low</span> | {cve['bugzilla']} | {cve['statement']} |\n")
