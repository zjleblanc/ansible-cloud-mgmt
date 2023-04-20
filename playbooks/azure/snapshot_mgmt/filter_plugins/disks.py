#!/usr/bin/python
from datetime import datetime, timedelta

class FilterModule(object):
    def filters(self):
        return {
            'date_offset': self.get_date_offset,
            'past_retention': self.filter_past_retention,
        }
    
    def get_date_offset(self, offset_days, date=datetime.now()):
        return (date + timedelta(days=int(offset_days))).strftime('%a %b %d %Y %H:%M:%S')

    def filter_past_retention(self, snapshots, offset_days=0):
        past_retention = []
        for snap in snapshots:
            retention_days = int(snap['tags']['retention'][:-1])
            expiry_date = datetime.now() + timedelta(days=offset_days) - timedelta(days=retention_days)
            created_date = datetime.strptime(snap['tags']['createdOn'], '%Y%m%d-%H%M%S')
            if created_date < expiry_date:
                snap['age'] = (datetime.now() + timedelta(days=offset_days) - created_date).days
                past_retention.append(snap)
        return past_retention