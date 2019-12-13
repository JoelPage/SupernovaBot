print("snEvents/event.py")
# Generic
import xml_helpers as snXMLHelpers
# Events
import snEvents.uid as snUID
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
            self.id = snUID.get()
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
        if self.end != None:
            snXMLHelpers.create_and_set_node_text_int(eventNode, 'end', self.end.timestamp())
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
            snXMLHelpers.set_attrib_text(signupNode, 'user', key)
            snXMLHelpers.set_attrib_text(signupNode, 'reaction', value)

    def deserialise(self, node):
        self.name = snXMLHelpers.get_value_text(node, 'name')
        self.id = snXMLHelpers.get_value_text(node, 'id')
        self.start = snXMLHelpers.get_value_datetime(node, 'start')
        self.end = snXMLHelpers.get_value_datetime(node, 'end')
        self.started = snXMLHelpers.get_value_bool(node, 'started')
        self.thumbnail = snXMLHelpers.get_value_text(node, 'thumbnail')
        self.image = snXMLHelpers.get_value_text(node, 'image')
        self.description = snXMLHelpers.get_value_text(node, 'description')
        remindedNode = snXMLHelpers.get_node(node, 'reminded')
        snXMLHelpers.get_values_float(remindedNode, 'reminder', self.reminded)
        self.signupMessageID = snXMLHelpers.get_value_int(node, 'signupmessageid')
        signupsNode = snXMLHelpers.get_node(node, 'signups')
        signupNodes = snXMLHelpers.get_nodes(signupsNode, 'signup')
        if signupNodes  != None:
            for signupNode in signupNodes:
                userId = snXMLHelpers.get_attrib_int(signupNode, 'user')
                print(userId)
                reaction = snXMLHelpers.get_attrib_text(signupNode, 'reaction')
                print(reaction)
                self.signups[userId] = reaction

    def get_embed_description(self):
        day = self.start.day
        month = self.start.month
        monthStr = snHelpers.get_month_as_string_abbr(month)
        hours = self.start.hour
        minutes = self.start.minute

        sDateTime = ""
        sDateTime = f"<{monthStr} {day}, {hours:02d}:{minutes:02d}"
        if self.end != None:
            endDay = self.end.day
            endMonth = self.end.month
            endMonthStr = snHelpers.get_month_as_string_abbr(endMonth)
            endHours = self.end.hour
            endMinutes = self.end.minute
            monthStr = ""
            if self.end.day != self.start.day or self.end.month != self.start.month:
                monthStr = f"{endMonthStr} {endDay}, "
            sDateTime = f"{sDateTime} - {monthStr}{endHours:02d}:{endMinutes:02d}>"
        else:
            sDateTime = f"{sDateTime}>"
        sDateTime = f"```xl\n{sDateTime}```"

        return f"{sDateTime}\n{self.description}"