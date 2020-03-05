
print("snEvents/events.py")
# This file is used to import snEvents in a clean way.
import snEvents.event as event
import snEvents.commands as commands
import snEvents.manager as manager
import snEvents.helpers as helpers
# Classes
Event = event.Event
# Variables
config = manager.m_config
# Functions
check_events = manager.check_events
get_events = manager.get_events
get_signup_channel_id = manager.get_signup_channel_id