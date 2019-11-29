import snEvents.event as event
import snEvents.commands as commands
import snEvents.manager as manager
import snEvents.helpers as helpers
# Classes
Event = event.Event
# Variables
events = manager.m_events
config = manager.m_config
# Functions
check_events = manager.check_events


#import command_manager as i_command_manager
#import event_commands as i_event_commands
#import event_globals as i_event_globals
#import event as i_event
#
#import unique_identifier as i_uid
#import helpers as i_util
#import xml.etree.ElementTree as i_tree
#import input as i_input
#
#import time as i_time
#import datetime as i_datetime
#
#import shlex as i_shlex
#
## Testing
#def createDummyEvent():
#    #print("createDummyEvent")
#    i_event_globals.eventsArray.clear()
#    firstEvent = createNewEvent("First Event", i_time.time())
#    i_event_globals.eventsArray.append(firstEvent)
#    dummyEventsTree = createTreeFromEventsArray(i_event_globals.eventsArray)
#    i_util.xml_helpers.fileWrite(dummyEventsTree, "events.xml")
#    i_event_globals.eventsArray.clear()
#
## Core Functions
#def initialiseEventsSystem():
#    #print("initialiseEventsSystem")
#    eventsTree = i_util.xml_helpers.fileRead("events.xml")
#    createEventsArrayFromTree(eventsTree.getroot())
#
#def createEventsArrayFromTree(treeRoot):
#    #print("createEventsArrayFromTree")
#    i_event_globals.eventsArray.clear()
#    for events in treeRoot.findall("events"):
#        for event in events.findall("event"):
#            eventName = event.find("name").text
#            uid = event.find("uid").text
#            start = int(i_time.time()) #int(event.find("start_time").text) # Ghetto Parse
#            i_event_globals.eventsArray.append(createEvent(uid, eventName, start))
#
#def createTreeFromEventsArray(array):
#    #print(f"createTreeFromEventsArray({array} Count:{len(array)}")
#    root = createEventTree()
#    for event in array:
#        addEventToTree(root, event)
#
#    return root
#
#def createEventTree():
#    #print("createEventTree")
#    root = i_tree.Element('root')
#    i_tree.SubElement(root, 'events')
#    return root
#
#def createNewEvent(name, start):
#    #print(f"createNewEvent({name})")
#    return i_event.Event(name, start)
#
#def createEvent(uid, name, start):
#    #print(f"createNewEvent({uid}, {name})")
#    return i_event.Event(name, start, uid=uid)
#
#def addEventToTree(treeRoot, event):
#    #print("addEventToTree")
#    events = treeRoot.find('events')
#    newEvent = i_tree.SubElement(events, 'event')
#    eventName = i_tree.SubElement(newEvent, 'name')
#    eventName.text = event.name
#    eventUID = i_tree.SubElement(newEvent, 'uid')
#    eventUID.text = event.uid
#    eventStartTime = i_tree.SubElement(newEvent, 'start_time')
#    eventStartTime.text = f"{event.start}"
#
#def writeEventsToFile(root):
#    #print("writeEventsToFile")
#    i_util.xml_helpers.fileWrite(root, "events.xml")
#
#def readEventsFromFile():
#    #print("readEventsFromFile")
#    i_util.xml_helpers.fileRead("events.xml")
#
#def findEventByUID(uid):
#    for event in i_event_globals.eventsArray:
#        if event.uid == uid:
#            return event
#
#    return None
#
#def isEnoughArgs(args, count):
#    return len(args) >= count
#
#def processArguments(args):
#    print(f"processArguments({args})")
#    if isEnoughArgs(args, 1):
#        executeCommand(args[0], args[1:])
#    else:
#        print("No input found")
#
#def executeCommand(command, args):
#    print(f"executeCommand({command}, {args})")
#    commandData = commandSwitch(command)
#
#    if commandData == None:
#        print("Unrecognised Command!")
#        return
#
#    if isEnoughArgs(args, commandData[1]):
#        commandData[0](args)
#    else:
#        print("Not enough arguments for command!")
#
#def commandSwitch(command):
#    switch = { 
#    "exit" : (commandExit, 0),
#    "list" : (commandList, 0),
#    "remove" : (commandRemove, 1),
#    "create" : (commandCreate, 2) }
#    return switch.get(command)
#
#def commandExit(args):
#    global g_exit
#    g_exit = True
#
#def commandList(args):
#    print(f"There are {len(g_eventsArray)} events:")
#    for event in g_eventsArray:
#        print(f"{event.uid}:{event.name}")
#
#def commandRemove(args):
#    uid = args[0] # Arg0 is the UID of the event to remove
#    print(f"Removing Event with UID:{uid}")
#    # TODO : Can we use a dictionary instead and remove by index?
#    foundEvent = findEventByUID(uid)
#    if foundEvent == None:
#        print(f"No event found with UID:{uid}") 
#    else:
#        g_eventsArray.remove(foundEvent)
#        tree = createTreeFromEventsArray(g_eventsArray)
#        writeEventsToFile(tree)
#        print(f"Event with UID:{uid} removed!")    
#        
#def parseTimeArgument(arg):
#    # Parse Text Time into Hours and Minutes
#    # 20:30 -> (20, 30)
#
#    splitArg = arg.split(":")
#    if len(splitArg) < 2:
#        print("Failed to parse Start Time")
#        return (0,0)
#    else:
#        hours = int(splitArg[0][0:2])
#        minutes = int(splitArg[1][0:2])
#        
#        # Validate hours and minutes
#        # less than 24 greater than 0
#        # less than 60 greater than 0
#        
#        return (hours, minutes)
#
#    # TODO : Specified AM/PM ?
#    # string ends with am/pm ?
#    # ToUpper    
#
#def commandCreate(args):
#    name = args[0] # Arg0 is the Name of the event
#    startTime = args[1] # Arg1 is the Start Time of the event
#    print(f"Creating Event {name} at {startTime}")
#
#    startTimeTuple = parseTimeArgument(startTime)
#
#    # Create Date with Specified Time
#    nowDateTime = i_datetime.datetime.now()
#    eventStartTime = nowDateTime.replace(hour=startTimeTuple[0], minute=startTimeTuple[1], second=0, microsecond=0)
#    eventStartTimeStamp = eventStartTime.timestamp()
#
#    # Check for duplicate UID
#    maxTries = 5
#    tries = 0
#    validEvent = False
#    newEvent = None
#    while validEvent == False | tries <= maxTries:
#        newEvent = createNewEvent(name, eventStartTimeStamp)
#        foundEvent = findEventByUID(newEvent.uid)
#        if foundEvent == None:
#            validEvent = True
#
#    if newEvent == None:
#        print("Invalid Event")
#        return
#
#    # handle end time first
#    # as non recursive optional argument
#    # parse time, if parse fails
#    # pass rest of args to recursive optional args
#
#    print(f"Handle optional arguments.")
#
#    # recursive function with switch?
#    # start-date date
#    # end-date
#
#
#    commandCreateOptionalArgs(newEvent, args[2:])
#
#    g_eventsArray.append(newEvent)
#    tree = createTreeFromEventsArray(g_eventsArray)
#    writeEventsToFile(tree)
#
#
#
#    return
#
#    # Optional Arguments
#    # For args[2:]
#
#    # We should handle the following args as option arguments
#    # Recursive function maybe?
#    # Create the event and pass it to this recursive function
#
#
#    # Parse End Time if Valid
#
#    # Parse Start Date
#    # If valid replace date in startdate
#
#    # Parse End Date
#    # If valid replace date in startdate
#
#    # Validate Start and End
#    # If start/end has already passed, event is invalid
#    # If no end then time is always valid
#
#    #if nowDateTime.timestamp() > eventStartTimeStamp:
#        # Event has already started.
#        # Is this okay?
#
#    # if nowDateTime.timestamp() > 
#
#    if validEvent == True:
#        
#        writeEventsToFile()
#    else:
#        print("Event was invalid!")
#    
#def commandCreateOptionalArgs(event, args):
#    if len(args) <= 0:
#        return
#    
#    arg = args[0]
#
## Core
#initialiseEventsSystem()
#
#while i_event_globals.exit == False:
#    print("Waiting for command...")
#    input = i_input.gatherInput()
#    args = i_shlex.split(input)
#    commandName = args[0]
#    i_command_manager.executeCommand(commandName, args[1:])
#    continue
#
#    # Edit
#    if command == "edit":        
#        print(f"Editing Event {arg1}")
#        foundEvent = findEventByUID(arg1)
#        if foundEvent == None:
#            print(f"No event found with UID {arg1}")
#        else:
#            print(f"Event with UID {arg1} Found!")
#            
#        continue
#
## Times for all events to allow sorting.
## Skip (Remove next upcoming event)
## More event values, Thumbnail, Image, Description, Members
#
#