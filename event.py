import unique_identifier as i_uid
import datetime as i_datetime
import time as i_time

class Event():
    def __init__(self, name, start, 
    uid=None, end=None, startDate=None, endDate=None):
        #print(f"Event({uid}, {name}, {start}, {end})")
        if uid == None:
            self.uid = i_uid.get()
        else:
            self.uid = uid

        self.name = name

        if startDate != None:
            gmStartDate = i_time.gmtime(startDate.timestamp())
            self.start = start.replace(year=gmStartDate.tm_year, month=gmStartDate.tm_mon, day=gmStartDate.tm_mday)    
        else:
            self.start = start

        if end != None and endDate == None: 
            gmStart = i_time.gmtime(self.start.timestamp())
            self.end = end.replace(year=gmStart.tm_year, month=gmStart.tm_mon, day=gmStart.tm_mday)
        elif end == None and endDate != None:
            gmStart = i_time.gmtime(self.start.timestamp())
            self.end = end.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
        elif end != None and endDate != None:
            gmEnd = i_time.gmtime(end.timestamp())
            self.end = endDate.replace(hour=gmEnd.tm_hour, minute=gmEnd.tm_min)
