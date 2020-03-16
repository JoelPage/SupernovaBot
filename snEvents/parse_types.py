# Python Includes
import argparse as i_argparse
import time as i_time
import datetime as i_datetime
# Supernova Events
import snEvents.helpers as snHelpers
# Aliases
helpers = snHelpers

def parse_time(string):
    if string == None: 
        raise ValueError("\nFailed to parse time!\nNo time provided.")

    splitString = string.split(":")

    if len(splitString) != 2: 
        raise ValueError(f"\nFailed to parse time!\nCould not understand {string} as Hours:Minutes.")

    if len(splitString[0]) < 1 or len(splitString[0]) > 2:
        raise ValueError(f"\nFailed to parse time!\nCould not understand {string} as Hours:Minutes.")

    if len(splitString[1]) != 2 and len(splitString[1]) != 4:
        raise ValueError("\nFailed to parse time!\nInvalid time format format!\nPlease use 13:37 or 13:37pm.")

    isPM = splitString[1].upper().endswith("PM")
    splitString[1] = splitString[1][:2]

    if len(splitString[1]) < 2:
        raise ValueError("\nFailed to parse time!\nNot enough digits to represent minutes.")

    parser = i_argparse.ArgumentParser(description="Parse Time")
    parser.add_argument("hours", type=int)
    parser.add_argument("minutes", type=int)
    args = parser.parse_args(splitString)

    if isPM:
        if args.hours < 12 : args.hours +=12

    if args.hours < 0 or args.hours > 24:
        raise ValueError("\nFailed to parse time!\nHours provided was greater than 24.")

    if args.minutes < 0 or args.minutes > 60:
        raise ValueError("\nFailed to parse time!\nMinutes provided was greater than 60.")

    now = snHelpers.get_now_offset()
    return now.replace(hour=args.hours, minute=args.minutes, second=0, microsecond=0)
        
def parse_date(string):
    if string == None: 
        raise ValueError("\nFailed to parse date!\nNo date was provided.")

    splitString = string.split("/")

    if len(splitString) < 2 or len(splitString) > 3:
        raise ValueError(f"\nFailed to parse date!\nCould not understand {string} as a date.")

    hasYear = len(splitString) == 3

    parser = i_argparse.ArgumentParser(description="Parse Date")
    parser.add_argument("day", type=int)
    parser.add_argument("month", type=int)
    if hasYear : parser.add_argument("year", type=int)
    args = parser.parse_args(splitString)

    if args.month < 0 or args.month > 12: 
        raise ValueError("\nFailed to parse month!\nMonth provided was greater than 12.")
    if args.day < 0 or args.day > 31: 
        raise ValueError("\nFailed to parse day!\nDay provided was greater than 31.")

    year = 1970
    if hasYear == False:
        now = helpers.get_now_offset()
        gmtime = i_time.gmtime(now.timestamp())
        year = gmtime.tm_year
    else:
        if args.year < 1970:
            raise ValueError("\nFailed to parse year!\nYear provided was less than 1970.")

    return i_datetime.datetime(year, args.month, args.day)

def parse_day(string):
    try:
        # Parse Day/Month
        pass
    except ValueError: raise i_argparse.ArgumentTypeError(f"\nFailed to parse day!")

def parse_uid(string):
    try:
        idLength = len(format(int(i_time.time()), 'X'))
        if idLength == len(string):
            return string
        else:
            raise ValueError
    except ValueError: raise i_argparse.ArgumentTypeError(f"\nFailed to parse event ID!\n An event ID must be {idLength} characters long.")

def parse_day_hour_minute(string):
    try:
        pass
    except ValueError:
        raise i_argparse.ArgumentTypeError(f"\nFailed to parse day/hour/minute!")
        
def parse_channel(string):
    try:
        if string.startswith('<#') and string.endswith('>'):
            print(string[2:len(string)-1])
            return int(string[2:len(string)-1])
        else:
            raise ValueError
    except ValueError: raise i_argparse.ArgumentTypeError(f"\nFailed to parse channel!\nUse the # key for a list of valid channels.")    

def parse_url(string):
    try:
        # TODO : Actually apply some validation here lol
        return string
    except ValueError: raise i_argparse.ArgumentTypeError(f"\nFailed to parse url!")

def parse_user(string):
    try:
        if string.startswith('<@!') and string.endswith('>'):
            return int(string[3:len(string)-1])
        else: raise ValueError
    except ValueError: raise i_argparse.ArgumentTypeError(f"\nFailed to parse user!\n Use the @ key for a list of valid users.\nIf the user is not in this channel go to one and copy paste their user tag.")

def parse_reaction(string):
    try:
        return string
    except ValueError: raise i_argparse.ArgumentTypeError(f"\nFailed to parse reaction!")
