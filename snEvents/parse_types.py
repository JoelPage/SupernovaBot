# Python Includes
import argparse as i_argparse
import time as i_time
import datetime as i_datetime
# Supernova Events
import snEvents.helpers as snHelpers
# Aliases
helpers = snHelpers

def parse_time(string):
    print("parse_time()")
    if string == None: 
        raise ValueError("No string provided")

    splitString = string.split(":")

    if len(splitString) != 2: 
        raise ValueError("Could not understand Hours:Minutes")

    if len(splitString[0]) < 1 or len(splitString[0]) > 2: 
        raise ValueError("Invalid time please provide Hours:Minutes")

    isPM = splitString[1].upper().endswith("PM")
    splitString[1] = splitString[1][:2]

    if len(splitString[1]) < 2:
        raise ValueError("Not enough digits to represent minutes")

    parser = i_argparse.ArgumentParser(description="Parse Time")
    parser.add_argument("hours", type=int)
    parser.add_argument("minutes", type=int)
    args = parser.parse_args(splitString)

    if isPM:
        if args.hours < 12 : args.hours +=12

    if args.hours < 0 or args.hours > 24: 
        raise ValueError("Hours provided was greater than 24")

    if args.minutes < 0 or args.minutes > 60:
        raise ValueError("Minutes provided was greater than 60")

    now = helpers.getNowWithOffset()
    return now.replace(hour=args.hours, minute=args.minutes, second=0, microsecond=0)
        
def parse_date(string):
    if string == None: 
        raise ValueError("No date was provided")

    splitString = string.split("/")

    if len(splitString) < 2 or len(splitString) > 3:
        raise ValueError("Could not understand hours:minutes")

    hasYear = len(splitString) == 3

    parser = i_argparse.ArgumentParser(description="Parse Date")
    parser.add_argument("day", type=int)
    parser.add_argument("month", type=int)
    if hasYear : parser.add_argument("year", type=int)
    args = parser.parse_args(splitString)

    if args.month < 0 or args.month > 12: 
        raise ValueError("Month provided was greater than 12")
    if args.day < 0 or args.day > 31: 
        raise ValueError("Day provided was greater than 31")

    year = 1970
    if hasYear == False:
        now = helpers.getNowWithOffset()
        gmtime = i_time.gmtime(now.timestamp())
        year = gmtime.tm_year
    else:
        if args.year < 1970:
            raise ValueError("Year provided was less than 1970")

    return i_datetime.datetime(year, args.month, args.day)

def parse_day(string):
    try:
        # Parse Day/Month
        pass
    except ValueError: raise i_argparse.ArgumentTypeError(f"Failed to parse day")

def parse_uid(string):
    try:
        if len(format(int(i_time.time()), 'X')) == len(string):
            return string
        else:
            raise ValueError
    except ValueError: raise i_argparse.ArgumentTypeError(f"Failed to parse UID")

def parse_day_hour_minute(string):
    try:
        pass
    except ValueError:
        raise i_argparse.ArgumentTypeError(f"Failed to parse day/hour/minute")
        
def parse_channel(string):
    try:
        if string.startswith('<#') and string.endswith('>'):
            print(string[2:len(string)-1])
            return string[2:len(string)-1]
        else:
            raise ValueError
    except ValueError: raise i_argparse.ArgumentTypeError(f"Failed to parse channel")    

def parse_url(string):
    try:
        return string
    except ValueError: raise i_argparse.ArgumentTypeError(f"Failed to parse url")
