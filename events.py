import uid
import helpers

import xml.etree.ElementTree as ET

# Testing
def CreateDummyEvent():
    print("CreateDummyEvent")
    eventsArray.clear()
    firstEvent = CreateNewEvent("First Event")
    eventsArray.append(firstEvent)
    dummyEventsTree = CreateTreeFromEventsArray(eventsArray)
    helpers.xml_helpers.fileWrite(dummyEventsTree, "events.xml")
    eventsArray.clear()

# Core Functions
def InitialiseEventsSystem():
    print("InitialiseEventsSystem")

    CreateDummyEvent()

    eventsTree = helpers.xml_helpers.fileRead("events.xml")
    CreateEventsArrayFromTree(eventsTree.getroot())

def CreateEventsArrayFromTree(treeRoot):
    print("CreateEventsArrayFromTree")
    eventsArray.clear()
    for events in treeRoot.findall("events"):
        for event in events.findall("event"):
            _eventName = event.find("name").text
            _uid = event.find("uid").text
            eventsArray.append(CreateEvent(_uid, _eventName))

def CreateTreeFromEventsArray(_array):
    print(f"CreateTreeFromEventsArray({_array} Count:{len(_array)}")
    root = CreateEventTree()
    for event in _array:
        AddEventToTree(root, event)

    return root

def CreateEventTree():
    print("CreateEventTree")
    root = ET.Element('root')
    ET.SubElement(root, 'events')
    return root

def CreateNewEvent(_name):
    print(f"CreateNewEvent({_name})")
    return Event(None, _name)

def CreateEvent(_uid, _name):
    print(f"CreateNewEvent({_uid}, {_name})")
    return Event(_uid=_uid, _name=_name)

def AddEventToTree(treeRoot, event):
    print("AddEventToTree")
    events = treeRoot.find('events')
    newEvent = ET.SubElement(events, 'event')
    eventName = ET.SubElement(newEvent, 'name')
    eventName.text = event.name
    eventUID = ET.SubElement(newEvent, 'uid')
    eventUID.text = event.uid

def WriteEventsToFile():
    helpers.xml_helpers.fileWrite(eventsTree, "events.xml")

def ReadEventsFromFile():
    helpers.xml_helpers.fileRead("events.xml")

# Initialise - Create File if no Exists
#              If file does exist load into memory
#              Keep tree in memory
#               
# Functions  - Add Event to Tree
#              - Report that an event is being created
#              - Add to in memory tree
#              - Export tree to file
#              - Report UID of created event
#            - List Events
#              - Convert events to text
#              - Display text in console
#              - Display text in discord
#            - Remove Event from Tree
#              - Remove from in memory tree
#              - Export tree to file
#            - Edit Event
#              - Find sub element in tree with matching ID
#              - Change name of event
#              - Export tree to file

# Event Structure
# UID 
# Name 
# Description - Optional 
# Start Date Time - Optional 
# End Date Time  - Optional 
class Event(object):
    
    def __init__(self, _uid=None, _name=None, _start=None, _end=None):
        print(f"Event({_uid}, {_name}, {_start}, {_end})")

        if _uid == None:
            self.uid = uid.get()
        else:
            self.uid = _uid

        if _name == None:
            self.name = _uid
        else:
            self.name = _name
        
        self.start = _start
        self.end = _end
      
#evnt = Event("test")
#print("Test Event :")
#print(evnt.uid)
#print(evnt.name)

# Core
eventsArray = []
eventsTree = None

InitialiseEventsSystem()

eventsTree = CreateTreeFromEventsArray(eventsArray)

