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
Event = snEvent.Event
Reminder = snReminder.Reminder
# Could we use a Dictionary ?
# Maybe if looping gets slow
m_xmlFilePath = "events.xml"
m_config = snConfig.Config()
m_events = []
m_exit = False
m_onEventDeletedAsync = helpers.delegate1
m_onEventCreatedAsync = helpers.delegate1
m_removedEvents = []

def initialise():
    helpers.debug_print("initialise()")
    deserialise()

def deserialise():
    helpers.debug_print("deserialise()")
    eventsTree = xml_helpers.fileRead(m_xmlFilePath)
    create_config_from_tree(eventsTree.getroot())
    create_events_from_tree(eventsTree.getroot())

def create_config_from_tree(treeRoot):
    helpers.debug_print(f"create_config_from_tree({treeRoot})")
    configNode = treeRoot.find("config")
    # Channels
    signupsNode = configNode.find("signups")
    if signupsNode != None:
        m_config.m_signupChannel = signupsNode.text
        
    announcementsNode = configNode.find("announcements")
    if announcementsNode != None:
        m_config.m_announcementChannel = announcementsNode.text
        
    logsNode = configNode.find('logs')
    if logsNode != None:
        m_config.m_logsChannel = logsNode.text
    # Sort Order
    sortOrderNode = configNode.find('sortorder')
    if sortOrderNode != None:
        m_config.m_isAscendingSort = True if sortOrderNode.text == "Ascending" else False
    # Time
    utcOffsetNode = configNode.find("utcoffset")
    m_config.m_utcOffset = float(utcOffsetNode.text)
    # Reminders
    m_config.m_reminders.clear()
    remindersNode = configNode.find("reminders")
    if remindersNode != None:
        reminderNodes = remindersNode.findall("reminder")
        for reminderNode in reminderNodes:
            hours = float(reminderNode.attrib["hours"])
            m_config.m_reminders.append(Reminder(hours=hours))
    # Reactions
    m_config.m_reactions.clear()
    reactionsNode = configNode.find("reactions")
    if reactionsNode != None:
        reactionNodes = reactionsNode.findall("reaction")
        for reactionNode in reactionNodes:
            emojiAsInt = int(reactionNode.attrib["emoji"])
            emojiAsBytes = emojiAsInt.to_bytes(3, sys.byteorder)
            emojiAsUnicode = emojiAsBytes.decode("utf-8")
            value = reactionNode.attrib["value"]
            m_config.m_reactions[emojiAsUnicode] = value

def create_events_from_tree(root):
    global m_events
    m_events.clear()
    # Events Node
    for events in root.findall("events"):
        # Event Node
        for event in events.findall("event"):
            # Create new event, call deserialise, pass node.
            newEvent = Event("Awaiting Deserialisation", helpers.get_now_offset())
            newEvent.deserialise(event)

            # Code bellow needs to be moved into deserialise function
            eventName = event.find("name").text
            id = event.find("id").text
            start = datetime.fromtimestamp(int(event.find("start").text))
            end = None
            endNode = event.find("end")
            if endNode != None:
                end = datetime.fromtimestamp(int(endNode.text))
            started = False
            startedNode = event.find("started")
            if startedNode != None:
                started = True if startedNode.text == "True" else False
            thumbnail = None
            thumbnailNode = event.find("thumbnail")
            if thumbnailNode != None:
                thumbnail = thumbnailNode.text
            image = None
            imageNode = event.find("image")
            if imageNode != None:
                image = imageNode.text
            description = None
            descriptionNode = event.find("description")
            if descriptionNode != None:
                description = descriptionNode.text
            reminded = []
            remindedNode = event.find("reminded")
            if remindedNode != None:
                for reminder in remindedNode.findall("reminder"):
                    reminded.append(float(reminder.text))
            signupMessageID = None
            signupMessageIDNode = event.find("signupmessageid")
            if signupMessageIDNode != None:
                signupMessageID = int(signupMessageIDNode.text)
            signups = {}
            signupsNode = event.find("signups")
            if signupsNode != None:
                signupNodes = signupsNode.findall("signup")
                for signupNode in signupNodes:
                    userId = int(signupNode.attrib["user"])
                    reaction = signupNode.attrib["reaction"]
                    signups[userId] = reaction

            m_events.append(Event(eventName, start, id=id, end=end, started=started, 
            description=description, image=image, thumbnail=thumbnail, reminded=reminded,
            signupMessageID=signupMessageID, signups=signups))

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
    tree.SubElement(root, 'config')
    tree.SubElement(root, 'events')
    return root

def add_config_to_tree(root):
    config = root.find('config')
    # Channels
    announcementsNode = tree.SubElement(config, 'announcements')
    announcementsNode.text = m_config.m_announcementChannel
    signupsNode = tree.SubElement(config, 'signups')
    signupsNode.text = m_config.m_signupChannel
    logsNode = tree.SubElement(config, 'logs')
    logsNode.text = m_config.m_logsChannel
    # Sort Order
    sortOrderNode = tree.SubElement(config, 'sortorder')
    sortOrderNode.text = "Ascending" if m_config.m_isAscendingSort == True else "Descending"
    # Time
    utcoffsetNode = tree.SubElement(config, 'utcoffset')
    utcoffsetNode.text = f"{m_config.m_utcOffset}"
    # Reminders
    remindersNode = tree.SubElement(config, 'reminders')
    for reminder in m_config.m_reminders:
        reminderNode = tree.SubElement(remindersNode, 'reminder')
        reminderNode.set('hours', f"{reminder.hours}")
        if reminder.message != None:
            reminderNode.set('message', reminder.message)
    # Reactions
    reactionsNode = tree.SubElement(config, 'reactions')
    for key, value in m_config.m_reactions.items():
        reactionNode = tree.SubElement(reactionsNode, 'reaction')
        emojiAsBytes = key.encode('utf8')
        emojiAsInt = int.from_bytes(emojiAsBytes, sys.byteorder)
        reactionNode.set('emoji', f"{emojiAsInt}")
        reactionNode.set('value', value)

def add_events_to_tree(root):
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
    reminderCheckResults = check_event_reminders()
    results.append(reminderCheckResults)

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

def check_event_reminders():
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

initialise()