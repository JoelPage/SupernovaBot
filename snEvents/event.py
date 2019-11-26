import snEvents.uid as uid

class Event():
    def __init__(self, name, start, id=None, end=None, started=False, 
    reminded=None, description=None, image=None, thumbnail=None,
    signupMessageID=None, rosterMessageID=None, signups=None):
        #print(f"Event({uid}, {name}, {start}, {end})")
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

        # WIP
        self.repeat = []
        self.announcements = []
        # Discord Specific
        self.signupMessageID = signupMessageID
        self.rosterMessageID = rosterMessageID