import event_globals as i_event_globals
import event_commands as i_event_commands

import event as i_event

import helpers as i_util

import time as i_time
import datetime as i_datetime

import xml.etree.ElementTree as i_tree

def initialise():
    #print("initialise")
    eventsTree = i_util.xml_helpers.fileRead("events.xml")
    createEventsArrayFromTree(eventsTree.getroot())

def publish():
    sortEvents()
    treeRoot = createTreeFromEventsArray(i_event_globals.eventsArray)
    writeEventsToFile(treeRoot)

def createTreeFromEventsArray(array):
    #print(f"createTreeFromEventsArray({array} Count:{len(array)}")
    root = createEventTree()
    for event in array:
        addEventToTree(root, event)

    return root

def writeEventsToFile(root):
    #print("writeEventsToFile")
    i_util.xml_helpers.fileWrite(root, "events.xml")

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
    
def findEventByUID(uid):
    for event in i_event_globals.eventsArray:
        if event.uid == uid:
            return event

    return None

def removeEvent(uid):
    resultStr = "Something went wrong."
    foundEvent = findEventByUID(uid)
    if foundEvent == None:
        resultStr = "No event found with UID:{uid}"
    else:
        i_event_globals.eventsArray.remove(foundEvent)
        publish()
        resultStr = f"Event named:{foundEvent.name} with UID:{uid} removed!"

    print(resultStr)
    return resultStr

def addEventToTree(treeRoot, event):
    #print("addEventToTree")
    events = treeRoot.find('events')
    newEvent = i_tree.SubElement(events, 'event')
    eventName = i_tree.SubElement(newEvent, 'name')
    eventName.text = event.name
    eventUID = i_tree.SubElement(newEvent, 'uid')
    eventUID.text = event.uid
    eventStart = i_tree.SubElement(newEvent, 'start')
    eventStart.text = f"{int(event.start.timestamp())}"
    if event.end != None:
        eventEnd = i_tree.SubElement(newEvent, "end")
        eventEnd.text = f"{int(event.end.timestamp())}"

def createEventsArrayFromTree(treeRoot):
    #print("createEventsArrayFromTree")
    i_event_globals.eventsArray.clear()
    for events in treeRoot.findall("events"):
        for event in events.findall("event"):
            eventName = event.find("name").text
            uid = event.find("uid").text
            start = i_datetime.datetime.fromtimestamp(int(event.find("start").text))
            end = None
            endNode = event.find("end")
            if endNode != None:
                end = i_datetime.datetime.fromtimestamp(int(endNode.text))
            i_event_globals.eventsArray.append(i_event.Event(eventName, start, uid=uid, end=end))
    
    sortEvents()

def sortEvents():
    i_event_globals.eventsArray.sort(key=eventSortFunc)

def eventSortFunc(event):
    return event.start.timestamp()

def readEventsFromFile():
    #print("readEventsFromFile")
    i_util.xml_helpers.fileRead("events.xml")

initialise()