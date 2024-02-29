from datetime import datetime, timezone

class FilterModule(object):

    def filters(self):
        return { "last_snapshot": self.do_last_snapshot }

    def do_last_snapshot(self, guest_snapshots):
        if not len(guest_snapshots):
          return -1
        
        latest = datetime.strptime(guest_snapshots['current_snapshot']['creation_time'], '%Y-%m-%dT%H:%M:%S.%f%z')
        return (datetime.now(timezone.utc) - latest).days
