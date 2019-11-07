import unique_identifier as i_uid

class Event():
    def __init__(self, name, start, 
    uid=None, end=None, started=False):
        #print(f"Event({uid}, {name}, {start}, {end})")
        if uid == None:
            self.uid = i_uid.get()
        else: 
            self.uid = uid
        self.name = name
        # Validated
        self.start = start
        self.end = end
        # WIP
        self.thumbnail = None
        self.image = None
        self.description = None
        self.repeat = None
        self.announcements = []
        # Flags
        self.started = started