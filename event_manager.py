import event_globals as i_event_globals
import event_commands as i_event_commands

import event as i_event

import helpers as i_util

import time as i_time

import xml.etree.ElementTree as i_tree

def initialise():
    #print("initialise")
    eventsTree = i_util.xml_helpers.fileRead("events.xml")
    createEventsArrayFromTree(eventsTree.getroot())

def createEventsArrayFromTree(treeRoot):
    #print("createEventsArrayFromTree")
    i_event_globals.eventsArray.clear()
    for events in treeRoot.findall("events"):
        for event in events.findall("event"):
            eventName = event.find("name").text
            uid = event.find("uid").text
            start = int(i_time.time()) #int(event.find("start_time").text) # Ghetto Parse
            i_event_globals.eventsArray.append(createEvent(uid, eventName, start))

def createTreeFromEventsArray(array):
    #print(f"createTreeFromEventsArray({array} Count:{len(array)}")
    root = createEventTree()
    for event in array:
        addEventToTree(root, event)

    return root

def createEventTree():
    #print("createEventTree")
    root = i_tree.Element('root')
    i_tree.SubElement(root, 'events')
    return root

def createNewEvent(name, start):
    #print(f"createNewEvent({name})")
    return i_event.Event(name, start)

def createEvent(uid, name, start):
    #print(f"createNewEvent({uid}, {name})")
    return i_event.Event(name, start, uid=uid)

    
def addEventToTree(treeRoot, event):
    #print("addEventToTree")
    events = treeRoot.find('events')
    newEvent = i_tree.SubElement(events, 'event')
    eventName = i_tree.SubElement(newEvent, 'name')
    eventName.text = event.name
    eventUID = i_tree.SubElement(newEvent, 'uid')
    eventUID.text = event.uid
    eventStartTime = i_tree.SubElement(newEvent, 'start_time')
    eventStartTime.text = f"{event.start}"

def writeEventsToFile(root):
    #print("writeEventsToFile")
    i_util.xml_helpers.fileWrite(root, "events.xml")

def readEventsFromFile():
    #print("readEventsFromFile")
    i_util.xml_helpers.fileRead("events.xml")

initialise()