# Serialisation
import xml.etree.ElementTree as tree
# Unique Identifier
import snEvents.uid as uid
# XML Helpers
import xml_helpers as snXMLHelpers
# General Helpers
import snEvents.helpers as snHelpers

class Event():
    # Do we need such an explicit constructor?
    def __init__(self, 
                 name, 
                 start, 
                 id=None, 
                 end=None, 
                 started=False, 
                 reminded=None, 
                 description=None, 
                 image=None, 
                 thumbnail=None,
                 signupMessageID=None,
                 signups=None):

        if id == None:
            self.id = uid.get()
        else: 
            self.id = id

        # Strings
        self.name = name
        self.thumbnail = thumbnail
        self.image = image
        self.description = description

        # Validated
        self.start = start
        self.end = end

        # Flags
        self.started = started
        self.isDirty = True

        # Array of Floats representing reminders
        if reminded == None:
            self.reminded = []
        else:
            self.reminded = reminded
        
        if signups == None:
            self.signups = {}
        else: 
            self.signups = signups

        # Discord Specific
        self.signupMessageID = signupMessageID

    def serialise(self, root):
        # Create a new node for this event in the tree
        eventsNode = root.find('events')
        eventNode = snXMLHelpers.create_node(eventsNode, 'event')
        # Begin adding members to the new event element
        snXMLHelpers.create_and_set_node_text(eventNode, 'name', self.name)
        snXMLHelpers.create_and_set_node_text(eventNode, 'id', self.id)
        snXMLHelpers.create_and_set_node_text_int(eventNode, 'start', self.start.timestamp())
        snXMLHelpers.create_and_set_node_text_int_if_exists(eventNode, 'end', self.end.timestamp())
        snXMLHelpers.create_and_set_node_text_bool(eventNode, 'started', self.started)
        snXMLHelpers.create_and_set_node_text_if_exists(eventNode, 'thumbnail', self.thumbnail)
        snXMLHelpers.create_and_set_node_text_if_exists(eventNode, 'image', self.image)
        snXMLHelpers.create_and_set_node_text_if_exists(eventNode, 'description', self.description)
        remindedNode = snXMLHelpers.create_node_if_exists(eventNode, 'reminded', self.reminded)
        snXMLHelpers.create_and_set_nodes_text(remindedNode, 'reminder', self.reminded)
        snXMLHelpers.create_and_set_node_text_if_exists(eventNode, 'signupmessageid', self.signupMessageID)
        signupsNode = snXMLHelpers.create_node(eventNode, 'signups')
        for key, value in self.signups.items():
            signupNode = snXMLHelpers.create_node(signupsNode, 'signup')
            signupNode.set("user", f"{key}")
            signupNode.set("reaction", value)

    def deserialise(self, node):
        snXMLHelpers.set_value_from_node_text(node, 'name', self.name)
        snXMLHelpers.set_value_from_node_text(node, 'id', self.id)
        # Start
        snXMLHelpers.set_value_from_node_datetime
        startAsString = node.find("start").text
        startAsInt = int(startAsString)
        self.start = snHelpers.datetime.fromtimestamp(startAsInt)
        # End
        endNode = node.find("end")
        if endNode != None:
            endAsString = endNode.text
            endAsInt = int(endAsString) 
            self.end = snHelpers.datetime.fromtimestamp(endAsInt)
        # Started
        startedNode = node.find("started")
        if startedNode != None:
            startedAsString = startedNode.text
            self.started = True if startedAsString == "True" else False
        # Thumbnail 
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