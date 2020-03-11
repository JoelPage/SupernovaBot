print("snEvents/manager.py")
# Python Includes
import sys
import time
import datetime as pyDateTime
import xml.etree.ElementTree as tree
# Supernova Events Includes
import snEvents.event as snEvent
import snEvents.helpers as snEventHelpers
import snEvents.config as snConfig
import snEvents.reminder as snReminder
import xml_helpers
# Module Aliases
helpers = snEventHelpers
datetime = pyDateTime.datetime
timedelta = pyDateTime.timedelta
# Class Aliases
print("Attempting to set Event Alias")
Event = snEvent.Event
print(f"Event alias set to {Event}")
Reminder = snReminder.Reminder
# Could we use a Dictionary ?
# Maybe if looping gets slow
m_xmlFilePath = "events.xml"
m_events = [] # TODO : use a class and not a global variable
m_exit = False
m_onEventDeletedAsync = helpers.delegate1
m_onEventCreatedAsync = helpers.delegate1
m_removedEvents = []

def initialise():
    helpers.debug_print("initialise()")

    global m_config
    m_config = snConfig.m_config

    deserialise()

def deserialise():
    helpers.debug_print("deserialise()")
    try:
        eventsTree = xml_helpers.fileRead(m_xmlFilePath)
        create_config_from_tree(eventsTree.getroot())
        create_events_from_tree(eventsTree.getroot())
    except Exception:
        helpers.debug_print("Failed to read xml, recreating with defaults")
        publish()

def create_config_from_tree(root):
    helpers.debug_print(f"create_config_from_tree({root})")
    m_config.deserialise(root)

def create_events_from_tree(root):
    clear_events()
    for eventsNode in root.findall("events"):
        for eventNode in eventsNode.findall("event"):
            newEvent = Event("Awaiting Deserialisation", helpers.get_now_offset())
            newEvent.deserialise(eventNode)
            add_event(newEvent)

    sort_events()

def sort_events():
    helpers.debug_print("sort_events()")
    m_events.sort(key=event_sort_by)

def event_sort_by(event):
    helpers.debug_print(f"event_sort_by({event})")
    return event.start.timestamp()

def publish():
    helpers.debug_print("publish()")
    sort_events()
    serialise()

def serialise():
    helpers.debug_print("serialise()")
    treeRoot = create_tree()
    write_tree_to_file(treeRoot)

def create_tree():
    root = initialise_tree()
    add_config_to_tree(root)
    add_events_to_tree(root)
    return root

def initialise_tree():
    root = tree.Element('root')
    return root

def add_config_to_tree(root):
    m_config.serialise(root)

def add_events_to_tree(root):
    tree.SubElement(root, 'events')
    for event in m_events:
        event.serialise(root)

def add_event_to_tree(root, event):
    helpers.debug_print(f"addEventsToTree({root},{event})")
    eventsNode = root.find('events')
    eventNode = tree.SubElement(eventsNode, 'event')
    nameNode = tree.SubElement(eventNode, 'name')
    nameNode.text = event.name
    idNode = tree.SubElement(eventNode, 'id')
    idNode.text = event.id
    startNode = tree.SubElement(eventNode, 'start')
    startNode.text = f"{int(event.start.timestamp())}"
    if event.end != None:
        endNode = tree.SubElement(eventNode, "end")
        endNode.text = f"{int(event.end.timestamp())}"
    startedNode = tree.SubElement(eventNode, 'started')
    startedNode.text = "True" if event.started else "False"
    if event.thumbnail != None:
        thumbnailNode = tree.SubElement(eventNode, "thumbnail")
        thumbnailNode.text = event.thumbnail
    if event.image != None:
        imageNode = tree.SubElement(eventNode, "image")
        imageNode.text = event.image
    if event.description != None:
        descNode = tree.SubElement(eventNode, "description")
        descNode.text = event.description
    if event.reminded != None:
        remindedNode = tree.SubElement(eventNode, "reminded")
        for reminded in event.reminded:
            reminderNode = tree.SubElement(remindedNode, "reminder")
            reminderNode.text = f"{reminded}"
    if event.signupMessageID != None:
        signupMsgIdNode = tree.SubElement(eventNode, "signupmessageid")
        signupMsgIdNode.text = f"{event.signupMessageID}"
    signupsNode = tree.SubElement(eventNode, "signups")
    for key, value in event.signups.items():
        signupNode = tree.SubElement(signupsNode, "signup")
        signupNode.set("user", f"{key}")
        signupNode.set("reaction", value)

def write_tree_to_file(root):
    xml_helpers.fileWrite(root, m_xmlFilePath)

def find_event_by_id(id):
    for event in m_events:
        if event.id == id:
            return event
    return None

def remove_event(event):
    helpers.debug_print(f"remove_event({event})")
    m_removedEvents.append(event)
    m_events.remove(event)
    publish()
    return f"Event {event.name} removed!"

def remove_event_by_id(id):
    helpers.debug_print(f"remove_event_by_id({id})")
    event = find_event_by_id(id)
    if event == None:
        return f"No event found with id:{id}"
    else:
        return remove_event(event)

def read_tree_from_file():
    xml_helpers.fileRead(m_xmlFilePath)

def check_events():
    # There are probably multiple things that need to happen here.
    # Check that events are still active.
    # Check reminders/announcements for events.
    # Possibly check for reactions to events.
    # Depending on the results of each check something different may need to be done
    # in discord by the bot.
    results = []
    # End Check
    endCheckResults = check_events_ending()
    results.append(endCheckResults)
    # Start Check
    startCheckResults = check_events_starting()
    results.append(startCheckResults)
    # Reminder Check
    reminderCheckResults = check_events_reminders()
    results.append(reminderCheckResults)
    # Lock Check
    lockCheckResults = check_events_lock()
    results.append(lockCheckResults)

    return results

def check_events_ending():
    removeResults = ["Events Removed as their endtime has passed."]
    now = helpers.get_now_offset()
    for event in m_events:
        if event.end != None and event.end < now:
            print(f"Event {event.id} {event.name} removed!")
            remove_event(event)
            removeResults.append(f":id: {event.id} {event.name}")
    if len(removeResults) > 1:
        publish()
        return removeResults
    else:
        return None

def check_events_starting():
    startResults = ["Events that started since the last check."]
    now = helpers.get_now_offset()
    for event in m_events:
        if event.started == False and event.start < now:
            startResults.append(f"{event.name}")
            event.started = True
    if len(startResults) > 1:
        publish()
        return startResults
    else:
        return None

def check_events_reminders():
    reminderResults = ["Events that have a reminder."]
    now = helpers.get_now_offset()
    for reminder in m_config.m_reminders:
        for event in m_events:
            if reminder.hours not in event.reminded:
                reminderDelta = timedelta(hours=reminder.hours)
                reminderTime = event.start - reminderDelta
                if now > reminderTime:
                    event.reminded.append(reminder.hours)
                    startDelta = event.start - now
                    reminderResults.append(f"{event.name} starts in {helpers.time_delta_to_string(startDelta)}")
    if len(reminderResults) > 1:    
        publish()
        return reminderResults
    else:
        return None

def check_events_lock():
    checkResults = []
    isDirty = False
    for event in m_events:
        if event.locked == False:
            if is_event_locked(event):
                event.locked = True
                checkResults.append(event)
                isDirty = True
    if isDirty:
        publish()
        return checkResults
    else:
        return None

def get_events():
    if m_config.m_isAscendingSort == True:
        return reversed(m_events)
    else:
        return m_events

def get_num_events():
    global m_events
    return len(m_events)

def add_event(event):
    global m_events
    m_events.append(event)

def clear_events():
    global m_events
    m_events.clear()

def get_signup_channel_id():
    return m_config.m_signupChannel

def is_event_locked(event):
    now = snEventHelpers.get_now_offset()
    if now > event.start:
        return True # already started
    signupLimitDelta = timedelta(hours=snConfig.m_config.m_signupLimit)
    lockTime = event.start - signupLimitDelta
    if now > lockTime:
        return True # event isn't locked
    return False


initialise()