# Python
import argparse
import datetime as pyDateTime
import time
# Supernova Commands
import snCommands.commands as commands
# Supernova Events
import snEvents.event as snEvent
import snEvents.manager as manager
import snEvents.parse_types as parse_types
import snEvents.helpers as helpers
import snEvents.reminder as snReminder
# Variable Aliases
m_events = manager.m_events
# Class Aliases
Event = snEvent.Event
Argument = commands.Argument
Result = commands.Result
Reminder = snReminder.Reminder
# Module Aliases
datetime = pyDateTime.datetime
timedelta = pyDateTime.timedelta
# Function Aliases
timeDeltaToString = helpers.timeDeltaToString

# TODO : This should be a generic command
class Command_Exit(commands.Command):
    def __init__(self):
        super().__init__("EXIT")

    def execute(self, args):
        manager.exit = True

Command_Exit()

class Command_Events(commands.Command):
    def __init__(self):
        super().__init__("EVENTS")

    def execute(self, args):
        results = [f"There are {len(m_events)} events:", ""]
        now = helpers.getNowWithOffset()
        for event in m_events:
            if event.start > now:
                timeDelta = event.start - now
                timeStr = timeDeltaToString(timeDelta)
                results[1] = f"{results[1]}:id:`{event.id}` ~ **{event.name}** Begins in {timeStr}\n" 
            else:
                if event.end != None:
                    timeDelta = event.end - now
                    timeStr = timeDeltaToString(timeDelta)
                    results[1] = f"{results[1]}:id:`{event.id}` ~ **{event.name}** Ends in {timeStr}\n"
                else:
                    results[1] = f"{results[1]}:id:`{event.id}` ~ **{event.name}** event has no end\n"
        return Result(value=results)

Command_Events()

class Command_Create(commands.Command):
    def __init__(self):
        super().__init__("CREATE")

    requiredArgs = [ 
        Argument("name", help="Set the name of the event. Format : 'Name in quotes'"),
        Argument("start", type=parse_types.parse_time, help="Set the start time. Format : HH:MM or H:MMam")
    ]

    optionalArgs = [
        Argument("start-date", type=parse_types.parse_date, help="Set the start date. Format : DD/MM or DD/MM/YYYY"),
        Argument("end-date", type=parse_types.parse_date, help="Set the end date. Format : DD/MM or DD/MM/YYYY"),
        Argument("end", type=parse_types.parse_time, help="Set the end time. Format : HH:MM or H:MMpm"),
        Argument("repeat", type=parse_types.parse_day, help="Set the days this event repeats. Format : 'Mon, Thu, Sun'"),
        Argument("expire", type=parse_types.parse_date, help="Set the date repeat expires. Format : DD/MM or DD/MM/YYYY"),
        Argument("description", help="Set the event description. Format : 'String in quotes'"),
        Argument("image", help="Set the event image. Format : 'String in quotes'"),
        Argument("thumbnail", help="Set the event thumbnail. Format : 'String in quotes'")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            now = helpers.getNowWithOffset()
            # Validate Start
            start = parsedArgs.start
            start_date = parsedArgs.start_date
            if start_date != None:
                gmStartDate = time.gmtime(start_date.timestamp())
                start = start.replace(year=gmStartDate.tm_year, month=gmStartDate.tm_mon, day=gmStartDate.tm_mday)
            if start < now:
                raise Exception("Start time is in the past!")
            # Validate End
            end = parsedArgs.end
            end_date = parsedArgs.end_date            
            if end != None and end_date == None: 
                gmStart = time.gmtime(start.timestamp())
                end = end.replace(year=gmStart.tm_year, month=gmStart.tm_mon, day=gmStart.tm_mday)
            elif end == None and end_date != None:
                gmStart = time.gmtime(start.timestamp())
                end = end.replace(hour=gmStart.tm_hour, minute=gmStart.tm_min)
            elif end != None and end_date != None:
                gmEnd = time.gmtime(end.timestamp())
                end = end_date.replace(hour=gmEnd.tm_hour, minute=gmEnd.tm_min)
            if end != None and end < start:
                raise Exception("End time is before start!")
                
            thumbnail = parsedArgs.thumbnail
            if thumbnail == None:
                thumbnail = manager.m_config.m_thumbnails[start.weekday()]
            
            image = parsedArgs.image

            newEvent = Event(parsedArgs.name, start, end=end, 
            description=parsedArgs.description, image=image, thumbnail=thumbnail)
            
            # If event is started past a reminder time, set as reminded
            for reminder in manager.m_config.m_reminders:
                reminderDelta = timedelta(hours=reminder.hours)
                reminderTime = newEvent.start - reminderDelta
                if reminderTime < now:
                    print(f"Adding Reminded for {reminder.hours}")
                    newEvent.reminded.append(reminder.hours)

            signups = {}
            for emoji in manager.m_signupEmojis:
                signups[emoji] = []

            m_events.append(newEvent)
            manager.publish()

            results = [f"New event created :id: {newEvent.id}"] 
            results.append(f'Title: "{newEvent.name}"\nStart: {newEvent.start}\nEnd: {newEvent.end}\nRepeat: {newEvent.repeat}\nDescription: "{newEvent.description}"')
            if newEvent.thumbnail != None:
                results[1] = f"{results[1]}\nThumbnail: '{newEvent.thumbnail}'"
            if newEvent.image != None:
                results[1] = f'{results[1]}\nImage: "{newEvent.image}"'

            print("Create Event Complete")

            return Result(value=results)

        except Exception as e:
            return Result(error=e.args[0])

Command_Create()

class Command_Skip(commands.Command):
    def __init__(self):
        super().__init__("SKIP")

    requiredArgs = [
        Argument("UID", type=parse_types.parse_uid, help="The UID of the Event to Skip")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            result = manager.removeEvent(parsedArgs.UID)

            return Result(value=result)
        except Exception as e:
            return Result(error=e.args)

Command_Skip()

class Command_Edit(commands.Command):
    def __init__(self):
        super().__init__("EDIT")

    requiredArgs = [
        Argument("UID", type=parse_types.parse_uid, help="The UID of the Event to Skip")
    ]

    optionalArgs = [
        Argument("name", help="Set the name of the event. Format : 'Name in quotes'"),
        Argument("start", type=parse_types.parse_time, help="Set the start time. Format : HH:MM or H:MMam"),
        Argument("end", type=parse_types.parse_time, help="Set the end time. Format : HH:MM or H:MMpm"),
        Argument("start-date", type=parse_types.parse_date, help="Set the start date. Format : DD/MM or DD/MM/YYYY"),
        Argument("end-date", type=parse_types.parse_date, help="Set the end date. Format : DD/MM or DD/MM/YYYY"),
        Argument("repeat", type=parse_types.parse_day, help="Set the days this event repeats. Format : 'Mon, Thu, Sun'"),
        Argument("expire", type=parse_types.parse_date, help="Set the date repeat expires. Format : DD/MM or DD/MM/YYYY"),
        Argument("description", help="Set the event description. Format : 'String in quotes'"),
        Argument("image", help="Set the event image. Format : 'String in quotes'"),
        Argument("thumbnail", help="Set the event thumbnail. Format : 'String in quotes'")
    ]

    def execute(self, args):
        try:
            print("ParseArgs")
            parsedArgs = self.parseArgs(args)
            print(f"Find Event {parsedArgs.UID}")
            foundEvent = manager.findEventByUID(parsedArgs.UID)
            if foundEvent == None:
                raise Exception(f"No event found with ID {parsedArgs.UID}")
            # String Updates
            if parsedArgs.name != None:
                foundEvent.name = parsedArgs.name
            if parsedArgs.description != None:
                foundEvent.description = parsedArgs.description
            if parsedArgs.image != None:
                foundEvent.image = parsedArgs.image
            if parsedArgs.thumbnail != None:
                foundEvent.thumbnail = parsedArgs.thumbnail
            # Time Updates            
            now = helpers.getNowWithOffset()
            # Start
            print("Validate Start")
            start = helpers.mergeTimeWithDateBase(foundEvent.start, parsedArgs.start, parsedArgs.start_date)
            if start != foundEvent.start:
                if start < now:
                    raise Exception(f"Start time is in the past!")
            # End
            print("Validate End")
            end = foundEvent.end
            if parsedArgs.end != None or parsedArgs.end_date != None:
                baseEnd = end
                if end == None:
                    baseEnd = start
                end = helpers.mergeTimeWithDateBase(baseEnd, parsedArgs.end, parsedArgs.end_date)
            if end != None:
                if end < start:
                    raise Exception(f"End is before start")
            foundEvent.start = start
            foundEvent.end = end
            # TODO : 
            # repeat
            # expire
            manager.publish()
            results = [f"Updated event :id: {foundEvent.id}"] 
            results.append(f'Title: "{foundEvent.name}"\nStart: {foundEvent.start}\nEnd: {foundEvent.end}\nRepeat: {foundEvent.repeat}\nDescription: "{foundEvent.description}"')
            if foundEvent.thumbnail != None:
                results[1] = f"{results[1]}\nThumbnail: '{foundEvent.thumbnail}'"
            if foundEvent.image != None:
                results[1] = f'{results[1]}\nImage: "{foundEvent.image}"'
            return Result(value=results)
        except Exception as e:
            return Result(error=e.args[0])

Command_Edit()

class Command_List(commands.Command):
    def __init__(self, args):
        super().__init__("LIST")

    requiredArgs = [
        Argument("UID", type=parse_types.parse_uid, help="The UID of the Event to Skip")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            foundEvent = manager.findEventByUID(parsedArgs.UID)
            result = []
            if foundEvent != None:
                # Print all users for each 'RSVP category'
                result.append(f"List some members.")
                pass
            else:
                result.append(f"No event found with UID {parsedArgs.UID}")
            
            return Result(value=result)
        except Exception as e:
            return Result(error=e.args)

# List cannot be implemented untill sign ups are implemented
class Command_Config_Reminder(commands.Command):
    def __init__(self):
        self.name = "reminder"

    requiredArgs = [
        Argument("addremove", choices=["add","remove"], help="Add or remove an event."),
        Argument("hours", type=float, help="The time in hours the reminder will be posted.")
    ]

    optionalArgs = [
        Argument("message", help="Custom message to be displayed when this reminder triggers.")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            return self.executeInternal(parsedArgs)
        except Exception as e:
            return Result(error=e.args)

    def executeInternal(self, args):
        if args.addremove == "add":
            manager.m_reminders.append(Reminder(args.hours, args.message))
            manager.publish()
            return Result(value=f"Reminder Added {args.hours} hours before events begin.")
        else:
            for reminder in manager.m_reminders:
                if reminder.hours == args.hours:
                    manager.m_reminders.remove(reminder)
                    manager.publish()
                    return Result(value=manager.m_reminders)

class Command_Config_Announcement(commands.Command):
    def __init__(self):
        self.name = "announcement"

    requiredArgs = [
        Argument("channel", type=parse_types.parse_channel, help="The name of the channel that announcements will be posted to")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            return self.executeInternal(parsedArgs)
        except Exception as e:
            return Result(error=e.args)

    def executeInternal(self, args):
        # Validate Channel? Maybe do that at a higher level?
        manager.m_config.m_announcementChannel = args.channel
        manager.publish()
        return Result(value=f"Announcements channel set to {args.channel}")

class Command_Config_Signup(commands.Command):
    def __init__(self):
        self.name = "signup"

    requiredArgs = [
        Argument("channel", type=parse_types.parse_channel, help="The name of the channel that signups will be posted to")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            return self.executeInternal(parsedArgs)
        except Exception as e:
            return Result(error=e.args)

    def executeInternal(self, args):
        # Validate Channel? Maybe do that at a higher level?
        manager.m_config.m_signupChannel = args.channel
        manager.publish()
        return Result(value=f"Signup channel set to {args.channel}")

class Command_Config_Logs(commands.Command):
    def __init__(self):
        self.name = "logs"

    requiredArgs = [
        Argument("channel", type=parse_types.parse_channel, help="The name of the channel that logs will be posted to")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            return self.executeInternal(parsedArgs)
        except Exception as e:
            return Result(error=e.args)

    def executeInternal(self, args):
        # Validate Channel? Maybe do that at a higher level?
        manager.m_config.m_logsChannel = args.channel
        manager.publish()
        return Result(value=f"Logs channel set to {args.channel}")

class Command_Config_Timezone(commands.Command):
    def __init__(self):
        self.name = "timezone"

    requiredArgs = [
        Argument("offset", type=float, help="The offset in hours from UTC")
    ]

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            return self.executeInternal(parsedArgs)
        except Exception as e:
            return Result(error=e.args)

    def executeInternal(self, args):
        # Validate this? Maybe keep less than +-12
        # In the future could add names of timezones or countries but not required
        manager.m_config.m_utcOffset = args.offset
        manager.publish()
        return Result(value=f"Timezone set to {args.offset}")

class Command_Config(commands.Command):
    def __init__(self):
        super().__init__("CONFIG")

    subCommands = [ 
        # Channels
        Command_Config_Announcement(),
        Command_Config_Signup(),
        Command_Config_Logs(),
        # Reminders
        Command_Config_Reminder(),
        # Time
        Command_Config_Timezone()
        ]

    def executeInternal(self, args):
        # Heading
        headingResult = ["Configuration"]
        # Channels - Convert to channel from channel ID
        channelsResult = ["Channels"]
        channelsResult.append(f"Announcements : <#{manager.m_config.m_announcementChannel}>")
        channelsResult.append(f"Signups : <#{manager.m_config.m_signupChannel}>")
        channelsResult.append(f"Logs : <#{manager.m_config.m_logsChannel}>")
        # Sort Order
        sortOrderResult = ["Sort Order"]
        sortOrderStr = "Ascending" if manager.m_config.m_isAscendingSort else "Descending"
        sortOrderResult.append(f"Sort Order : {sortOrderStr}")
        # Reminders
        remindersResult = ["Reminders"]
        for reminder in manager.m_config.m_reminders:
            remindersResult.append(f"{reminder.hours}")
        # Time
        utcoffsetResult = ["Time"]
        utcoffsetResult.append(f"UTC Offset : {manager.m_config.m_utcOffset}")
        # Reactions
        reactionsResult = ["Reactions"]
        reactionsResult.append(f"RSVP Reactions :\n")
        for key, value in manager.m_config.m_reactions.items():
            reactionsResult[1] = f"{reactionsResult[1]}{value} : {key}\n"

        result = [
            headingResult,
            channelsResult,
            sortOrderResult,
            remindersResult,
            utcoffsetResult,
            reactionsResult
            ]

        # Ghetto fix - formating
        formatedString = f"{result[0][0]}"
        # Channels
        formatedString = f"{formatedString}\n```xl\n// {result[1][0]}"
        for channelStr in result[1][1:]:
            formatedString = f"{formatedString}\n{channelStr}"
        formatedString = f"{formatedString}```"
        # Sort Order
        formatedString = f"{formatedString}\n```xl\n// {result[2][0]} \n{result[2][1:]}```"
        # Reminders
        formatedString = f"{formatedString}```xl\n// {result[3][0]} \n{result[3][1:]}```"
        # Time
        formatedString = f"{formatedString}```xl\n// {result[4][0]} \n{result[4][1]}```"
        # Reactions
        formatedString = f"{formatedString}```xl\n// {result[5][0]} \n{result[5][1]}```"

        return Result(value=formatedString)
Command_Config()
