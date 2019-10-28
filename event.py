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
        self.start = start

        if startDate != None:
            gmStartDate = i_time.gmtime(startDate.timestamp())
            self.start = start.replace(year=gmStartDate.tm_year, month=gmStartDate.tm_mon, day=gmStartDate.tm_mday)    

        if end != None and endDate == None: 
            gmNow = i_time.gmtime(i_datetime.datetime.now())
            self.end = end.replace(year=gmNow.tm_year, month=gmNow.tm_mon, day=gmNow.tm_mday)
        elif end == None and endDate != None:
            gmNow = i_time.gmtime(i_datetime.datetime.now())
            self.end = end.replace(hour=gmNow.tm_hour, minute=gmNow.tm_min)
        elif end != None and endDate != None:
            gmEndDate = i_time.gmtime(endDate.timestamp())
            self.end = end.replace(year=gmEndDate.tm_year, month=gmEndDate.tm_mon, day=gmEndDate.tm_mday)

        print(end)

        self.endDate = endDate
