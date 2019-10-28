import command as i_command
import event_globals as i_event_globals
import argument_parse_types as i_argument_parse_types
import argparse as i_argparse
import event as i_event
import event_manager as i_event_manager

class Command_Exit(i_command.Command):
    def __init__(self):
        super().__init__("EXIT")

    def execute(self, args):
        i_event_globals.exit = True

Command_Exit()

class Command_List(i_command.Command):
    def __init__(self):
        super().__init__("LIST")

    def execute(self, args):
        print(f"There are {len(i_event_globals.eventsArray)} events:")
        for event in i_event_globals.eventsArray:
            print(f"{event.uid}:{event.name}")

Command_List()

class Command_Create(i_command.Command):
    def __init__(self):
        super().__init__("CREATE")

    requiredArgs = { 
        i_command.Argument("name", help="Set the name of the event. Format : 'Name in quotes'"),
        i_command.Argument("start", type=i_argument_parse_types.parse_time, help="Set the start time. Format : HH:MM or H:MMam")
        }

    optionalArgs = {
        i_command.Argument("end", type=i_argument_parse_types.parse_time, help="Set the end time. Format : HH:MM or H:MMpm"),
        i_command.Argument("start-date", type=i_argument_parse_types.parse_date, help="Set the start date. Format : DD/MM or DD/MM/YYYY"),
        i_command.Argument("end-date", type=i_argument_parse_types.parse_date, help="Set the end date. Format : DD/MM or DD/MM/YYYY"),
        i_command.Argument("repeat", type=i_argument_parse_types.parse_day, help="Set the days this event repeats. Format : 'Mon, Thu, Sun'"),
        i_command.Argument("expire", type=i_argument_parse_types.parse_date, help="Set the date repeat expires. Format : DD/MM or DD/MM/YYYY"),
        i_command.Argument("description", help="Set the event description. Format : 'String in quotes'")
        }

    def execute(self, args):
        parsedArgs = self.parseArgs(args)
        newEvent = i_event.Event(parsedArgs.name, parsedArgs.start)

        newEvent.end = parsedArgs.end
        #newEvent.start_date = parsedArgs.start-date

        i_event_globals.eventsArray.append(newEvent)
        #i_event_manager.publish()


Command_Create()