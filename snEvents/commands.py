# Python
import argparse
import datetime as pyDateTime
import time
import calendar as pyCalendar
# Supernova Commands
import snCommands.commands as commands
# Supernova Events
import snEvents.event as snEvent
import snEvents.manager as manager
import snEvents.parse_types as parse_types
import snEvents.helpers as helpers
import snEvents.reminder as snReminder
# Class Aliases
Event = snEvent.Event
Argument = commands.Argument
Result = commands.Result
Reminder = snReminder.Reminder
# Module Aliases
datetime = pyDateTime.datetime
timedelta = pyDateTime.timedelta
# Function Aliases
time_delta_to_string = helpers.time_delta_to_string

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

    def executeInternal(self, args):
        results = [f"There are {manager.get_num_events()} events:", ""]
        now = helpers.get_now_offset()
        for event in manager.get_events():
            if event.start > now:
                timeDelta = event.start - now
                timeStr = time_delta_to_string(timeDelta)
                results[1] = f"{results[1]}:id:`{event.id}` ~ **{event.name}** Begins in {timeStr}\n" 
            else:
                if event.end != None:
                    timeDelta = event.end - now
                    timeStr = time_delta_to_string(timeDelta)
                    results[1] = f"{results[1]}:id:`{event.id}` ~ **{event.name}** Ends in {timeStr}\n"
                else:
                    results[1] = f"{results[1]}:id:`{event.id}` ~ **{event.name}** event has no end\n"
        return results

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
        Argument("expire", type=parse_types.parse_date, help="Set the date repeat expires. Format : DD/MM or DD/MM/YYYY"),
        Argument("description", help="Set the event description. Format : 'String in quotes'"),
        Argument("image", help="Set the event image. Format : 'String in quotes'"),
        Argument("thumbnail", help="Set the event thumbnail. Format : 'String in quotes'")
    ]

    def executeInternal(self, args):
        now = helpers.get_now_offset()
        # Validate Start
        start = args.start
        start_date = args.start_date
        if start_date != None:
            gmStartDate = time.gmtime(start_date.timestamp())
            start = start.replace(year=gmStartDate.tm_year, month=gmStartDate.tm_mon, day=gmStartDate.tm_mday)
        if start < now:
            raise Exception("Start time is in the past!")
        # Validate End
        end = args.end
        end_date = args.end_date            
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
            
        thumbnail = args.thumbnail
        if thumbnail == None:
            thumbnail = manager.m_config.m_thumbnails[start.weekday()]
        
        image = args.image

        newEvent = Event(args.name, start, end=end, 
        description=args.description, image=image, thumbnail=thumbnail)
        
        # If event is started past a reminder time, set as reminded
        for reminder in manager.m_config.m_reminders:
            reminderDelta = timedelta(hours=reminder.hours)
            reminderTime = newEvent.start - reminderDelta
            if reminderTime < now:
                print(f"Adding Reminded for {reminder.hours}")
                newEvent.reminded.append(reminder.hours)

        signups = {}
        for emoji in manager.m_config.m_reactions.keys():
            signups[emoji] = []

        manager.add_event(newEvent)
        manager.publish()

        results = [f"New event created :id: {newEvent.id}"] 
        results.append(f'Title: "{newEvent.name}"\nStart: {newEvent.start}\nEnd: {newEvent.end}\nDescription: "{newEvent.description}"')
        if newEvent.thumbnail != None:
            results[1] = f"{results[1]}\nThumbnail: '{newEvent.thumbnail}'"
        if newEvent.image != None:
            results[1] = f'{results[1]}\nImage: "{newEvent.image}"'

        return results

Command_Create()

class Command_Skip(commands.Command):
    def __init__(self):
        super().__init__("SKIP")

    requiredArgs = [
        Argument("UID", type=parse_types.parse_uid, help="The UID of the Event to Skip")
    ]

    def executeInternal(self, args):
        result = manager.remove_event_by_id(args.UID)
        return result

Command_Skip()

class Command_Edit_Signup(commands.Command):
    def __init__(self):
        self.name = "signup"

    requiredArgs = [
        Argument("addremove", choices=["add","remove"], help="Add or remove an event."),
        Argument("user", type=parse_types.parse_user, help="The user to add to or remove from the event signups."),
    ]

    optionalArgs = [
        Argument("reaction", type=parse_types.parse_reaction, help="The reaction to add/remove for the user to the event.")
    ]

    def executeInternal(self, args):
        # This is a unique case! We need perform an Async Function.
        return args

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
        Argument("expire", type=parse_types.parse_date, help="Set the date repeat expires. Format : DD/MM or DD/MM/YYYY"),
        Argument("description", help="Set the event description. Format : 'String in quotes'"),
        Argument("image", help="Set the event image. Format : 'String in quotes'"),
        Argument("thumbnail", help="Set the event thumbnail. Format : 'String in quotes'")
    ]

    subCommands = [
        Command_Edit_Signup()
    ]

    def executeInternal(self, args):
        print("Edit Command - Execute Internal")
        foundEvent = manager.find_event_by_id(args.UID)
        if foundEvent == None:
            raise Exception(f"No event found with ID {args.UID}")
        foundEvent.isDirty = True
        # String Updates
        if args.name != None:
            foundEvent.name = args.name
        if args.description != None:
            foundEvent.description = args.description
        if args.image != None:
            foundEvent.image = args.image
        if args.thumbnail != None:
            foundEvent.thumbnail = args.thumbnail
        # Time Updates            
        now = helpers.get_now_offset()
        # Start
        start = helpers.merge_time_with_date_base(foundEvent.start, args.start, args.start_date)
        if start != foundEvent.start:
            if start < now:
                raise Exception(f"Start time is in the past!")
        # End
        end = foundEvent.end
        if args.end != None or args.end_date != None:
            baseEnd = end
            if end == None:
                baseEnd = start
            end = helpers.merge_time_with_date_base(baseEnd, args.end, args.end_date)
        if end != None:
            if end < start:
                raise Exception(f"End is before start")
        foundEvent.start = start
        foundEvent.end = end

        manager.publish()
        results = [f"Updated event :id: {foundEvent.id}"] 
        results.append(f'Title: "{foundEvent.name}"\nStart: {foundEvent.start}\nEnd: {foundEvent.end}\nDescription: "{foundEvent.description}"')
        if foundEvent.thumbnail != None:
            results[1] = f"{results[1]}\nThumbnail: '{foundEvent.thumbnail}'"
        if foundEvent.image != None:
            results[1] = f'{results[1]}\nImage: "{foundEvent.image}"'
        return results

Command_Edit()

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

    def executeInternal(self, args):
        if args.addremove == "add":
            manager.m_config.m_reminders.append(Reminder(args.hours, args.message))
            manager.publish()
            return [ [ "Reminders", f"Reminder Added {args.hours} hours before events begin." ] ]
        else:
            for reminder in manager.m_config.m_reminders:
                if reminder.hours == args.hours:
                    manager.m_config.m_reminders.remove(reminder)
                    manager.publish()
                    return [ [ "Reminders", f"Reminder {args.hours} has been removed." ] ]
        
        raise Exception(f"Reminder {args.hours} could not be found.")

class Command_Config_Announcement(commands.Command):
    def __init__(self):
        self.name = "announcement"

    requiredArgs = [
        Argument("channel", type=parse_types.parse_channel, help="The name of the channel that announcements will be posted to")
    ]

    def executeInternal(self, args):
        manager.m_config.m_announcementChannel = args.channel
        manager.publish()
        return [ ["Announcements", f"Announcements channel set to <#{args.channel}>"] ]

class Command_Config_Signup(commands.Command):
    def __init__(self):
        self.name = "signup"

    requiredArgs = [
        Argument("channel", type=parse_types.parse_channel, help="The name of the channel that signups will be posted to")
    ]

    def executeInternal(self, args):
        # Validate Channel? Maybe do that at a higher level?
        manager.m_config.m_signupChannel = args.channel
        manager.publish()
        return [ [ "Signup", f"Signup channel set to <#{args.channel}>" ] ]

class Command_Config_Logs(commands.Command):
    def __init__(self):
        self.name = "logs"

    requiredArgs = [
        Argument("channel", type=parse_types.parse_channel, help="The name of the channel that logs will be posted to")
    ]

    def executeInternal(self, args):
        # Validate Channel? Maybe do that at a higher level?
        manager.m_config.m_logsChannel = args.channel
        manager.publish()
        return [ [ "Logs", f"Logs channel set to <#{args.channel}>" ] ]

class Command_Config_Heartbeat(commands.Command):
    def __init__(self):
        self.name = "heartbeat"

    requiredArgs = [
        Argument("channel", type=parse_types.parse_channel, help="The name of the channel that heartbeats will be posted to")
    ]

    def executeInternal(self, args):
        # Validate Channel? Maybe do that at a higher level?
        manager.m_config.m_heartbeatChannel= args.channel
        manager.publish()
        return [ [ "Heartbeat", f"Heartbeat channel set to <#{args.channel}>" ] ]


class Command_Config_Timezone(commands.Command):
    def __init__(self):
        self.name = "timezone"

    requiredArgs = [
        Argument("offset", type=float, help="The offset in hours from UTC")
    ]

    def executeInternal(self, args):
        # Validate this? Maybe keep less than +-12
        # In the future could add names of timezones or countries but not required
        manager.m_config.m_utcOffset = args.offset
        manager.publish()
        return [ [ "Timezone", f"Timezone set to {args.offset}" ] ]

class Command_Config_Signup_Limit(commands.Command):
    def __init__(self):
        self.name = "signuplimit"

    requiredArgs = [
        Argument("limit", type=float, help="The number of hours before the raid that signups will be locked.")
    ]

    def executeInternal(self, args):
        manager.m_config.m_signupLimit = args.limit
        manager.publish()
        return [ [ "Signup Limit", f"Signup limit set to {args.limit}" ] ]

class Command_Config_Debug(commands.Command):
    def __init__(self):
        self.name = "debug"

    requiredArgs = [
        Argument("channel", type=parse_types.parse_channel, help="The name of the channel that debug messages will be posted to.")
    ]

    def executeInternal(self, args):
        # Validate Channel? Maybe do that at a higher level?
        manager.m_config.m_debugChannel = args.channel
        manager.publish()
        return [ [ "Debug", f"Debug channel set to <#{args.channel}>" ] ]

class Command_Config_Sorting(commands.Command):
    def __init__(self):
        self.name = "sorting"

    requiredArgs = [
        Argument("order", choices=["asc","desc"], help="The order in which events will be sorted.")
    ]

    def executeInternal(self, args):
        if args.order == "asc":
            manager.m_config.m_isAscendingSort = True
        else:
            manager.m_config.m_isAscendingSort = False
        manager.publish()
        resultStr = "Ascending" if manager.m_config.m_isAscendingSort == True else "Descending"
        return [ [ "Sorting", resultStr ] ]

class Command_Config_Welcome_Message(commands.Command):
    def __init__(self):
        self.name = "welcome-message"

    requiredArgs = [
        Argument("message", help="A message to overwrite the old welcome message.")
    ]

    def executeInternal(self, args):
        manager.m_config.m_welcomeMessage = args.message
        manager.publish()
        return [ [ "Welcome Message", args.message ] ] 

class Command_Config(commands.Command):
    def __init__(self):
        super().__init__("CONFIG")

    subCommands = [ 
        # Channels
        Command_Config_Announcement(),
        Command_Config_Signup(),
        Command_Config_Logs(),
        Command_Config_Debug(),
        Command_Config_Heartbeat(),
        # Reminders
        Command_Config_Reminder(),
        # Time
        Command_Config_Timezone(),
        # Signup Limit
        Command_Config_Signup_Limit(),
        # Sorting
        Command_Config_Sorting(),
        # Welcome Message
        Command_Config_Welcome_Message()
        ]

    def executeInternal(self, args):
        # Channels - 
        channelsHeading = "Channels"
        channelsContent = f"""Announcements : <#{manager.m_config.m_announcementChannel}>
                              Signups       : <#{manager.m_config.m_signupChannel}>
                              Logs          : <#{manager.m_config.m_logsChannel}>
                              Debug         : <#{manager.m_config.m_debugChannel}>
                              Heartbeat     : <#{manager.m_config.m_heartbeatChannel}>"""
        channelsData = [channelsHeading, channelsContent]
        # Sort Order
        sortOrderHeading = "Sort Order"
        sortOrderContent = "Ascending" if manager.m_config.m_isAscendingSort else "Descending"
        sortOrderData = [sortOrderHeading, sortOrderContent]
        # Reminders
        remindersHeading = "Reminders"
        remindersContent = "0"
        for reminder in manager.m_config.m_reminders:
            remindersContent = f"{remindersContent}, {reminder.hours}"
        remindersData = [remindersHeading, remindersContent]
        # Time
        timeHeading = "Time"
        timeContent = f"UTC Offset: {manager.m_config.m_utcOffset} hours"
        timeData = [timeHeading, timeContent]
        # Signup Limit
        signupLimitHeading = "Signup Limit"
        signupLimitContent = f"Signup Limit: {manager.m_config.m_signupLimit} hours"
        signupLimitData = [signupLimitHeading, signupLimitContent]
        # Reactions
        reactionsHeading = "Reactions"
        reactionsContent = ""
        for key, value in manager.m_config.m_reactions.items():
            reactionsContent = f"{reactionsContent}{value} - {key}\n"
        reactionsData = [reactionsHeading, reactionsContent]
        # Thumbnails
        thumbnailsHeading = "Thumbnails"
        thumbnailsContent = ""
        for thumbnail in manager.m_config.m_thumbnails:
            index = manager.m_config.m_thumbnails.index(thumbnail)
            abbrDay = pyCalendar.day_abbr[index]
            thumbnailsContent = f"{thumbnailsContent}{abbrDay} - {thumbnail}\n"
        thumbnailsData = [thumbnailsHeading, thumbnailsContent]
        # Welcome Message
        welcomeMessageHeading = "Welcome Message"
        welcomeMessageContent = manager.m_config.m_welcomeMessage
        welcomeMessageData = [welcomeMessageHeading, welcomeMessageContent]

        result = [
            channelsData,
            sortOrderData,
            remindersData,
            timeData,
            signupLimitData,
            reactionsData,
            thumbnailsData,
            welcomeMessageData
            ]

        return result

Command_Config()