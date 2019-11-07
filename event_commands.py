import commands as i_commands

import argument_parse_types as i_argument_parse_types
import argparse as i_argparse

import event_globals as i_event_globals
import event as i_event
import event_manager as i_event_manager
import events as i_events

import datetime as i_datetime
import time as i_time

# This should be a generic command
class Command_Exit(i_commands.Command):
    def __init__(self):
        super().__init__("EXIT")

    def execute(self, args):
        i_event_globals.exit = True

Command_Exit()

class Command_Events(i_commands.Command):
    def __init__(self):
        super().__init__("EVENTS")

    def execute(self, args):
        # Detect if the event is already in progress, if it is when does it end?
        results = [f"There are {len(i_event_globals.eventsArray)} events:", ""]
        now = i_datetime.datetime.now()
        for event in i_event_globals.eventsArray:
            if event.start > now:
                #print(f"Get Time String For Event with name {event.name}")
                #print(event.start)
                #print(now)
                timeDelta = event.start - now
                timeStr = getTimeUntilStringFromTimeDelta(timeDelta)
                results[1] = f"{results[1]}:id:`{event.uid}` ~ **{event.name}** Begins in {timeStr}\n" 
            else:
                if event.end != None:
                    timeDelta = event.end - now
                    timeStr = getTimeUntilStringFromTimeDelta(timeDelta)
                    results[1] = f"{results[1]}:id:`{event.uid}` ~ **{event.name}** Ends in {timeStr}\n"
                else:
                    results[1] = f"{results[1]}:id:`{event.uid}` ~ **{event.name}** event has no end\n"

        return i_commands.Result(value=results)

# move to helpers
def getTimeUntilStringFromTimeDelta(td):
        tdDays = td.days
        tdHours = td.seconds//3600
        tdMinutes = (td.seconds//60)%60
        timeStr = ""

        #print(f"tdDays{tdDays}")
        #print(f"tdHours{tdHours}")
        #print(f"tdMinutes{tdMinutes}")

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

Command_Events()

class Command_Create(i_commands.Command):
    def __init__(self):
        super().__init__("CREATE")

    requiredArgs = [ 
        i_commands.Argument("name", help="Set the name of the event. Format : 'Name in quotes'"),
        i_commands.Argument("start", type=i_argument_parse_types.parse_time, help="Set the start time. Format : HH:MM or H:MMam")
    ]

    optionalArgs = [
        i_commands.Argument("end", type=i_argument_parse_types.parse_time, help="Set the end time. Format : HH:MM or H:MMpm"),
        i_commands.Argument("start-date", type=i_argument_parse_types.parse_date, help="Set the start date. Format : DD/MM or DD/MM/YYYY"),
        i_commands.Argument("end-date", type=i_argument_parse_types.parse_date, help="Set the end date. Format : DD/MM or DD/MM/YYYY"),
        i_commands.Argument("repeat", type=i_argument_parse_types.parse_day, help="Set the days this event repeats. Format : 'Mon, Thu, Sun'"),
        i_commands.Argument("expire", type=i_argument_parse_types.parse_date, help="Set the date repeat expires. Format : DD/MM or DD/MM/YYYY"),
        i_commands.Argument("description", help="Set the event description. Format : 'String in quotes'")
    ]

    def execute(self, args):
        try:
            print("Command Create")
            # Parse Args
            print("Parse Args")
            parsedArgs = self.parseArgs(args)
            # Cache some reusable variables
            now = i_datetime.datetime.now()
            print("Validate Args")
            # Validate Start
            start = parsedArgs.start
            start_date = parsedArgs.start_date
            if start_date != None:
                gmStartDate = i_time.gmtime(start_date.timestamp())
                start = start.replace(year=gmStartDate.tm_year, month=gmStartDate.tm_mon, day=gmStartDate.tm_mday)
            if start < now:
                raise Exception("Start time is in the past!")
            # Validate End
            end = parsedArgs.end
            end_date = parsedArgs.end_date            
            if end != None and end_date == None: 
                gmStart = i_time.gmtime(start.timestamp())
                end = end.replace(year=gmStart.tm_year, month=gmStart.tm_mon, day=gmStart.tm_mday)
            elif end == None and end_date != None:
                gmStart = i_time.gmtime(start.timestamp())
                end = end.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
            elif end != None and end_date != None:
                gmEnd = i_time.gmtime(end.timestamp())
                end = end_date.replace(hour=gmEnd.tm_hour, minute=gmEnd.tm_min)
            if end != None and end < start:
                raise Exception("End time is before start!")
                
            print("Create New Event")
            newEvent = i_event.Event(parsedArgs.name, start, end=end)

            newEvent.repeat = parsedArgs.repeat
            newEvent.expire = parsedArgs.expire
            newEvent.description = parsedArgs.description

            i_event_globals.eventsArray.append(newEvent)
            i_event_manager.publish()

            results = [f"New event created :id: {newEvent.uid}", ""] 
            results[1] = f"Title: '{newEvent.name}'\nStart: {newEvent.start}\nEnd: {newEvent.end}\nRepeat:{newEvent.repeat}\nDescription: '{newEvent.description}'"

            return i_commands.Result(value=results)

        except Exception as e:
            return i_commands.Result(error=e.args[0])

Command_Create()

class Command_Skip(i_commands.Command):
    def __init__(self):
        super().__init__("SKIP")

    requiredArgs = [
        i_commands.Argument("UID", type=i_argument_parse_types.parse_uid, help="The UID of the Event to Skip")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            result = i_event_manager.removeEvent(parsedArgs.UID)

            return i_commands.Result(value=result)
        except Exception as e:
            return i_commands.Result(error=e.args)

Command_Skip()

class Command_Edit(i_commands.Command):
    def __init__(self):
        super().__init__("EDIT")

    requiredArgs = [
        i_commands.Argument("UID", type=i_argument_parse_types.parse_uid, help="The UID of the Event to Skip")
    ]

    optionalArgs = [
        i_commands.Argument("name", help="Set the name of the event. Format : 'Name in quotes'"),
        i_commands.Argument("start", type=i_argument_parse_types.parse_time, help="Set the start time. Format : HH:MM or H:MMam"),
        i_commands.Argument("end", type=i_argument_parse_types.parse_time, help="Set the end time. Format : HH:MM or H:MMpm"),
        i_commands.Argument("start-date", type=i_argument_parse_types.parse_date, help="Set the start date. Format : DD/MM or DD/MM/YYYY"),
        i_commands.Argument("end-date", type=i_argument_parse_types.parse_date, help="Set the end date. Format : DD/MM or DD/MM/YYYY"),
        i_commands.Argument("repeat", type=i_argument_parse_types.parse_day, help="Set the days this event repeats. Format : 'Mon, Thu, Sun'"),
        i_commands.Argument("expire", type=i_argument_parse_types.parse_date, help="Set the date repeat expires. Format : DD/MM or DD/MM/YYYY"),
        i_commands.Argument("description", help="Set the event description. Format : 'String in quotes'"),
        i_commands.Argument("reminders", type=i_argument_parse_types.parse_day_hour_minute, help="Set reminders for this event. Format : The number of days/hours/minutes before the event a reminder will be set. '1d2h30m' ")
    ]

    def execute(self, args):
        try:
            print("ParseArgs")
            parsedArgs = self.parseArgs(args)
            print(f"Find Event {parsedArgs.UID}")
            foundEvent = i_event_manager.findEventByUID(parsedArgs.UID)
            if foundEvent == None:
                raise Exception(f"No event found with ID {parsedArgs.UID}")
            # String Updates
            if parsedArgs.name != None:
                foundEvent.name = parsedArgs.name
            if parsedArgs.description != None:
                foundEvent.description = parsedArgs.description
            # Time Updates            
            now = i_datetime.datetime.now()
            # Start
            start = i_events.time.mergeTimeWithDateBase(foundEvent.start, parsedArgs.start, parsedArgs.start_date)
            if start != foundEvent.start:
                if start < now:
                    raise Exception(f"Start time is in the past!")
            # End
            end = foundEvent.end
            print(parsedArgs.end)
            print(parsedArgs.end_date)
            if parsedArgs.end != None or parsedArgs.end_date != None:
                print("Editing end")
                baseEnd = end
                if end == None:
                    baseEnd = start
                end = i_events.time.mergeTimeWithDateBase(baseEnd, parsedArgs.end, parsedArgs.end_date)
            if end != None:
                if end < start:
                    raise Exception(f"End is before start")
            foundEvent.start = start
            foundEvent.end = end
            # TODO : 
            # repeat
            # expire
            i_event_manager.publish()
            results = [f"Updated event :id: {foundEvent.uid}"] 
            results.append(f"Title: '{foundEvent.name}'\nStart: {foundEvent.start}\nEnd: {foundEvent.end}\nRepeat:{foundEvent.repeat}\nDescription: '{foundEvent.description}'")
            return i_commands.Result(value=results)
        except Exception as e:
            return i_commands.Result(error=e.args[0])


Command_Edit()

class Command_List(i_commands.Command):
    def __init__(self, args):
        super().__init__("LIST")

    requiredArgs = [
        i_commands.Argument("UID", type=i_argument_parse_types.parse_uid, help="The UID of the Event to Skip")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            foundEvent = i_event_manager.findEventByUID(parsedArgs.UID)
            result = []
            if foundEvent != None:
                # Print all users for each 'RSVP category'
                result.append(f"List some members.")
                pass
            else:
                result.append(f"No event found with UID {parsedArgs.UID}")
            
            return i_commands.Result(value=result)
        except Exception as e:
            return i_commands.Result(error=e.args)


