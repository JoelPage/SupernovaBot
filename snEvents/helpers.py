print("snEvents/helpers.py")
# Python
import os as pyOs
import calendar as pyCalendar
import time as pyTime
import datetime as pyDatetime
import asyncio as pyAsyncio
from dotenv import load_dotenv
# Config
import snEvents.config as snConfig
# Aliases
datetime = pyDatetime.datetime
timedelta = pyDatetime.timedelta
# Variables
getTimeInMilliseconds = lambda: int(round(pyTime.time() * 1000))
# Delegates
def delegate1(a):
    print(f"delegate1({a})")

def delegate2(a, b):
    print(f"delegate2({a},{b})")

# Async
async def sleep_async(seconds):
    await pyAsyncio.sleep(seconds)

# Functions
def debug_print(message):
    now = get_now_time_string()
    print(f"{now} - {message}")

def get_month_as_string_abbr(month):
    return pyCalendar.month_abbr[month]

def get_discord_bot_token():
    load_dotenv()    
    return pyOs.getenv('DISCORD_TOKEN')

def get_now_offset():
    offsetHours = snConfig.m_config.m_utcOffset
    utcnow = datetime.utcnow()
    offsetDelta = timedelta(hours=offsetHours)
    return utcnow + offsetDelta

def merge_time_with_date_base(base,t,d):
    debug_print(f"merge_time_with_date_base({base},{t},{d})")
    if t != None and d != None:
        gmStart = pyTime.gmtime(t.timestamp())
        return d.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
    elif base != None:
        if t != None and d == None:
            gmStart = pyTime.gmtime(t.timestamp())
            return base.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
        elif t == None and d != None:
            gmStart = pyTime.gmtime(base.timestamp())
            return d.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
        else:
            return base
    elif t != None:
        return t
    elif d != None:
        return d
    else:
        return None

def time_delta_to_string(td):
    debug_print(f"time_delta_to_string({td})")
    # Insert 'and' between penultimate and ultimate string
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

def get_now_time_string():
    gmTimeNow = pyTime.gmtime(pyDatetime.datetime.now().timestamp())
    return f"{gmTimeNow.tm_hour:02d}:{gmTimeNow.tm_min:02d}"