# Python
import sys as pySys
# Generic
import xml_helpers as snXMLHelpers
# Reminder
import snEvents.reminder

class Config():   
    def __init__(self):
        # Reminders
        self.m_reminders = []
        # Channels
        self.m_debugChannel = 0
        self.m_announcementChannel = 0
        self.m_signupChannel = 0
        self.m_logsChannel = 0
        self.m_heartbeatChannel = 0
        # Sort Order
        self.m_isAscendingSort = False
        # Time
        self.m_utcOffset = 0
        self.m_signupLimit = 0
        # Signups
        self.m_reactions = { 
            "✅" : "Yes",
            "❔" : "Unsure",
            "❌" : "No" }
        # Default Daily Thumbnails
        self.m_thumbnails = [
            "https://i.imgur.com/sBFpHZ5.png", # Monday
            "https://i.imgur.com/06DdvTd.png", # Tuesday
            "https://i.imgur.com/eWgmroj.png", # Wednesday
            "https://i.imgur.com/sHfPSth.png", # Thursday
            "https://i.imgur.com/0lWrvhl.png", # Friday
            "https://i.imgur.com/cahcbdw.png", # Saturday
            "https://i.imgur.com/BwObwND.png"  # Sunday
        ]
        self.m_welcomeMessage = "Please set your nickname to be your in-game character name and leave us a message in #new-arrivals and we will get back to you!"

    def serialise(self, root):
        configNode = snXMLHelpers.create_node(root, 'config')
        snXMLHelpers.create_and_set_node_text_int(configNode, 'announcements', self.m_announcementChannel)
        snXMLHelpers.create_and_set_node_text_int(configNode, 'signups', self.m_signupChannel)
        snXMLHelpers.create_and_set_node_text_int(configNode, 'logs', self.m_logsChannel)
        snXMLHelpers.create_and_set_node_text_int(configNode, 'debug', self.m_debugChannel)
        snXMLHelpers.create_and_set_node_text_int(configNode, 'heartbeat', self.m_heartbeatChannel)
        snXMLHelpers.create_and_set_node_text_bool(configNode, 'ascendingsort', self.m_isAscendingSort)
        snXMLHelpers.create_and_set_node_text_float(configNode, 'utcoffset', self.m_utcOffset)
        snXMLHelpers.create_and_set_node_text(configNode, 'welcomemessage', self.m_welcomeMessage)
        snXMLHelpers.create_and_set_node_text_int(configNode, 'signuplimit', self.m_signupLimit)

        remindersNode = snXMLHelpers.create_node(configNode, 'reminders')
        for reminder in self.m_reminders:
            reminderNode = snXMLHelpers.create_node(remindersNode, 'reminder')
            snXMLHelpers.set_attrib_text(reminderNode, 'hours', reminder.hours)
            snXMLHelpers.set_attrib_text_if_exists(reminderNode, 'message', reminder.message)

        reactionsNode = snXMLHelpers.create_node(configNode, 'reactions')
        for key, value in self.m_reactions.items():
            reactionNode = snXMLHelpers.create_node(reactionsNode, 'reaction')
            snXMLHelpers.set_attrib_text_int_bytes(reactionNode, 'emoji', key)
            snXMLHelpers.set_attrib_text(reactionNode, 'value', value)

    def deserialise(self, node):
        configNode = snXMLHelpers.get_node(node, 'config')        
        sChannel = snXMLHelpers.get_value_int(configNode, 'signups')
        if sChannel != None:
            self.m_signupChannel = sChannel 
        aChannel = snXMLHelpers.get_value_int(configNode, 'announcements')
        if aChannel != None:
            self.m_announcementChannel = aChannel
        lChannel = snXMLHelpers.get_value_int(configNode, 'logs')
        if lChannel != None:
            self.m_logsChannel = lChannel
        dChannel = snXMLHelpers.get_value_int(configNode, 'debug')
        if dChannel != None: 
            self.m_debugChannel = dChannel
        hChannel = snXMLHelpers.get_value_int(configNode, 'heartbeat')
        if hChannel != None:
            self.m_heartbeatChannel = hChannel
        self.m_isAscendingSort = snXMLHelpers.get_value_bool(configNode, 'sortorder')
        self.m_utcOffset = snXMLHelpers.get_value_float(configNode, 'utcoffset')
        wMessage = snXMLHelpers.get_value_text(configNode, 'welcomemessage')
        if wMessage != None:
            self.m_welcomeMessage = wMessage
        self.m_signupLimit = snXMLHelpers.get_value_int(configNode, 'signuplimit')

        remindersNode = snXMLHelpers.get_node(configNode, 'reminders')
        reminderNodes = snXMLHelpers.get_nodes(remindersNode, 'reminder')
        self.m_reminders.clear()
        for reminderNode in reminderNodes:
            hours = snXMLHelpers.get_attrib_float(reminderNode, 'hours') 
            message = snXMLHelpers.get_attrib_text(reminderNode, 'message')
            reminder = snEvents.reminder.Reminder(hours=hours, message=message)
            self.m_reminders.append(reminder)

        reactionsNode = snXMLHelpers.get_node(configNode, 'reactions')
        reactionNodes = snXMLHelpers.get_nodes(reactionsNode, 'reaction')
        self.m_reactions.clear()
        for reactionNode in reactionNodes:
            emoji = snXMLHelpers.get_attrib_unicode(reactionNode, 'emoji')
            value = snXMLHelpers.get_attrib_text(reactionNode, 'value')
            self.m_reactions[emoji] = value

    def findReaction(self, v):
        for key, value in self.m_reactions.items():
            if value == v:
                return key

m_config = Config()