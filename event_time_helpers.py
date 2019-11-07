import time as i_time

def mergeTimeWithDateBase(base,time,date):
    if time != None and date != None:
        gmStart = i_time.gmtime(time.timestamp())
        return date.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
    elif base != None:
        if time != None and date == None:
            gmStart = i_time.gmtime(time.timestamp())
            return base.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
        elif time == None and date != None:
            gmStart = i_time.gmtime(base.timestamp())
            return date.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
        else:
            return base
    elif time != None:
        return time
    elif date != None:
        return date
    else:
        return None


