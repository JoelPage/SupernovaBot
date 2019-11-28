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
# Module Aliases
helpers = snEventHelpers
xml_helpers = snEventHelpers.xml_helpers
datetime = pyDateTime.datetime
timedelta = pyDateTime.timedelta
# Class Aliases
Event = snEvent.Event
Reminder = snReminder.Reminder
# Could we use a Dictionary ?
# Maybe if looping gets slow
m_xmlFilePath = "events.xml"
m_config = snConfig.Config()
m_reminders = []
m_events = []
m_exit = False
m_onEventDeletedAsync = helpers.delegate2
m_onEventCreatedAsync = helpers.delegate1

def initialise():
    deserialise()

def deserialise():
    print("Deserialising")
    eventsTree = xml_helpers.fileRead(m_xmlFilePath)
    createConfigFromTree(eventsTree.getroot())
    createEventsArrayFromTree(eventsTree.getroot())

def createConfigFromTree(treeRoot):
    configNode = treeRoot.find("config")
    # Channels
    signupsNode = configNode.find("signups")
    if signupsNode != None:
        m_config.m_signupChannel = signupsNode.text
    announcementsNode = configNode.find("announcements")
    if announcementsNode != None:
        m_config.m_announcementChannel = announcementsNode.text
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

def createEventsArrayFromTree(treeRoot):
    global m_events
    m_events.clear()
    for events in treeRoot.findall("events"):
        for event in events.findall("event"):
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
            rosterMessageID = None
            rosterMessageIDNode = event.find("rostermessageid")
            if rosterMessageIDNode != None:
                rosterMessageID = int(rosterMessageIDNode.text)
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
            signupMessageID=signupMessageID, rosterMessageID=rosterMessageID,
            signups=signups))
    sortEvents()

def sortEvents():
    m_events.sort(key=eventSortFunc)

def publish():
    sortEvents()
    serialise()

def serialise():
    print("Serialising")
    treeRoot = createTree()
    writeEventsToFile(treeRoot)

def createTree():
    root = initialiseTree()
    addConfigToTree(root)
    addEventsToTree(root)
    return root

def initialiseTree():
    root = tree.Element('root')
    tree.SubElement(root, 'config')
    tree.SubElement(root, 'events')
    return root

def addConfigToTree(root):
    config = root.find('config')
    # Channels
    announcementsNode = tree.SubElement(config, 'announcements')
    announcementsNode.text = m_config.m_announcementChannel
    signupsNode = tree.SubElement(config, 'signups')
    signupsNode.text = m_config.m_signupChannel
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

def addEventsToTree(root):
    for event in m_events:
        addEventToTree(root, event)

def addEventToTree(root, event):
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
    if event.rosterMessageID != None:
        rosterMsgIdNode = tree.SubElement(eventNode, "rostermessageid")
        rosterMsgIdNode.text = f"{event.rosterMessageID}"
    if event.signupMessageID != None:
        signupMsgIdNode = tree.SubElement(eventNode, "signupmessageid")
        signupMsgIdNode.text = f"{event.signupMessageID}"
    signupsNode = tree.SubElement(eventNode, "signups")
    print(event.signups)
    for key, value in event.signups.items():
        signupNode = tree.SubElement(signupsNode, "signup")
        signupNode.set("user", f"{key}")
        signupNode.set("reaction", value)

def writeEventsToFile(root):
    xml_helpers.fileWrite(root, m_xmlFilePath)

def findEventByUID(id):
    for event in m_events:
        if event.id == id:
            return event
    return None

def removeEvent(id):
    resultStr = "Something went wrong."
    foundEvent = findEventByUID(id)
    if foundEvent == None:
        resultStr = f"No event found with UID:{id}"
    else:
        # Push Message IDs to removal buffer
        m_events.remove(foundEvent)
        publish()
        
        resultStr = f"Event {id} {foundEvent.name} removed!"
    return resultStr

def eventSortFunc(event):
    return event.start.timestamp()

def readEventsFromFile():
    xml_helpers.fileRead(m_xmlFilePath)

async def checkEventsAsync():
    # There are probably multiple things that need to happen here.
    # Check that events are still active.
    # Check reminders/announcements for events.
    # Possibly check for reactions to events.
    # Depending on the results of each check something different may need to be done
    # in discord by the bot.
    results = []
    # End Check
    endCheckResults = await checkEventsEndingAsync()
    results.append(endCheckResults)
    # Start Check
    startCheckResults = checkEventsStarting()
    results.append(startCheckResults)
    # Reminder Check
    reminderCheckResults = checkEventReminders()
    results.append(reminderCheckResults)

    return results

async def checkEventsEndingAsync():
    removeResults = ["Events Removed as their endtime has passed."]
    now = helpers.getNowWithOffset()
    for event in m_events:
        if event.end != None and event.end < now:
            print(f"Event {event.id} {event.name} removed!")
            await m_onEventDeletedAsync(event.signupMessageID, event.rosterMessageID)
            m_events.remove(event)
            removeResults.append(f":id: {event.id} {event.name}")
    if len(removeResults) > 1:
        publish()
        return removeResults
    else:
        return None

def checkEventsStarting():
    startResults = ["Events that started since the last check."]
    now = helpers.getNowWithOffset()
    for event in m_events:
        if event.started == False and event.start < now:
            startResults.append(f"{event.name}")
            event.started = True
    if len(startResults) > 1:
        publish()
        return startResults
    else:
        return None

def checkEventReminders():
    reminderResults = ["Events that have a reminder."]
    now = helpers.getNowWithOffset()
    for reminder in m_config.m_reminders:
        for event in m_events:
            if reminder.hours not in event.reminded:
                reminderDelta = timedelta(hours=reminder.hours)
                reminderTime = event.start - reminderDelta
                if now > reminderTime:
                    event.reminded.append(reminder.hours)
                    startDelta = event.start - now
                    reminderResults.append(f"{event.name} starts in {helpers.timeDeltaToString(startDelta)}")
    if len(reminderResults) > 1:    
        publish()
        return reminderResults
    else:
        return None

initialise()