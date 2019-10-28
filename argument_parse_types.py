import argparse as i_argparse
import time as i_time
import datetime as i_datetime

def parse_time(string):
    try:
        if string == None: raise ValueError

        splitString = string.split(":")

        if len(splitString) != 2: raise ValueError

        if len(splitString[0]) < 1 or len(splitString[0]) > 2: raise ValueError

        isPM = splitString[1].upper().endswith("PM")
        splitString[1] = splitString[1][:2]

        if len(splitString[1]) < 2: raise ValueError

        parser = i_argparse.ArgumentParser(description="Parse Time")
        parser.add_argument("hours", type=int)
        parser.add_argument("minutes", type=int)
        args = parser.parse_args(splitString)

        if isPM:
            if args.hours < 12 : args.hours +=12

        if args.hours < 0 or args.hours > 24: raise ValueError

        if args.minutes < 0 or args.minutes > 60: raise ValueError

        nowDateTime = i_datetime.datetime.now()
        return nowDateTime.replace(hour=args.hours, minute=args.minutes, second=0, microsecond=0)

    except ValueError: raise i_argparse.ArgumentTypeError(f"Failed to parse {string} as time")
        
def parse_date(string):
    try:
        if string == None: raise ValueError

        splitString = string.split("/")

        if len(splitString) < 2 or len(splitString) > 3: raise ValueError 

        hasYear = len(splitString) == 3

        parser = i_argparse.ArgumentParser(description="Parse Date")
        parser.add_argument("day", type=int)
        parser.add_argument("month", type=int)
        if hasYear : parser.add_argument("year", type=int)
        args = parser.parse_args(splitString)

        if args.month < 0 or args.month > 12 : return ValueError
        if args.day < 0 or args.day > 31 : return ValueError

        year = 1970
        if hasYear == False:
            now = i_datetime.datetime.now()
            gmtime = i_time.gmtime(now.timestamp())
            year = gmtime.tm_year
        else:
            if args.year < 1970 : return ValueError

        return i_datetime.datetime(year, args.month, args.day)

    except ValueError: raise i_argparse.ArgumentTypeError(f"Failed to parse {string} as date")

def parse_day(string):
    try:
        # Parse Day/Month
        pass
    except ValueError: raise i_argparse.ArgumentTypeError(f"Failed to parse day")