# Python
import time
import datetime as pyDatetime
# General
import xml_helpers
import threading_helpers
# Supernova Events
import snEvents.manager as snManager
# Aliases
manager = snManager
datetime = pyDatetime.datetime
timedelta = pyDatetime.timedelta
# Variables
getTimeInMilliseconds = lambda: int(round(time.time() * 1000))
# Functions
def delegate1(a):
    print(f"delegate1({a})")

def delegate2(a, b):
    print(f"delegate2({a},{b})")

def getNowWithOffset():
    offsetHours = manager.m_config.m_utcOffset
    utcnow = datetime.utcnow()
    offsetDelta = timedelta(hours=offsetHours)
    return utcnow + offsetDelta

def CreateDummyEvent(fileName):
	xml_helpers.createDummyEvent(fileName) 	

def mergeTimeWithDateBase(base,t,d):
    print(base,t,d)
    if t != None and d != None:
        gmStart = time.gmtime(t.timestamp())
        return d.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
    elif base != None:
        if t != None and d == None:
            gmStart = time.gmtime(t.timestamp())
            return base.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
        elif t == None and d != None:
            gmStart = time.gmtime(base.timestamp())
            return d.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
        else:
            return base
    elif t != None:
        return t
    elif d != None:
        return d
    else:
        return None

def timeDeltaToString(td):
    # Insert and between penultimate and ultimate string
    tdDays = td.days
    tdHours = td.seconds//3600
    tdMinutes = (td.seconds//60)%60
    timeStr = ""
    if tdDays > 0 : 
        if tdDays == 1:
            timeStr = f"{timeStr}{tdDays} day "
        else:
            timeStr = f"{timeStr}{tdDays} days "
    if tdHours > 0 :
        if tdHours == 1:
            timeStr = f"{timeStr}{tdHours} hour "
        else:
            timeStr = f"{timeStr}{tdHours} hours "
    if tdMinutes > 0 :
        if tdMinutes == 1:
            timeStr = f"{timeStr}{tdMinutes} minute "
        else:
            timeStr = f"{timeStr}{tdMinutes} minutes "
    if tdDays == 0 and tdHours == 0 and tdMinutes == 0:
        if td.seconds == 1:
            timeStr = f"{timeStr}{td.seconds} second "
        else:
            timeStr = f"{timeStr}{td.seconds} seconds "
    return timeStr

def getNowTimeStr():
    gmTimeNow = time.gmtime(pyDatetime.datetime.now().timestamp())
    return f"{gmTimeNow.tm_hour:02d}:{gmTimeNow.tm_min:02d}"
#def CreateFunctionThread(func, args=None):
#	#print("Helpers - Creating Function Thread")
#	if args:
#		return threading_helpers.CreateThread(func, args)
#	else:
#		return threading_helpers.CreateThread(func)
#
#def CreateAndRunFunctionThread(func, args=None):
#	if args:
#		thread = CreateFunctionThread(func, args)
#	else:
#		thread = CreateFunctionThread(func)
#		
#	#print("Helpers - Starting Function Thread")
#	thread.start()
#	return thread
#	
#async def CreateFunctionThreadAsync(func, args=None):
#	#print("Helpers - Creating Function Thread")
#	if args:
#		return await threading_helpers.CreateThread(func, args)
#	else:
#		return await threading_helpers.CreateThread(func)
#
#async def CreateAndRunFunctionThreadAsync(func, args=None):
#	if args:
#		thread = await CreateFunctionThreadAsync(func, args)
#	else:
#		thread = await CreateFunctionThreadAsync(func)
#		
#	#print("Helpers - Starting Function Thread")
#	await thread.start()
#	return thread