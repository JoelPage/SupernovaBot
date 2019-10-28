import unique_identifier as i_uid

class Event():
    def __init__(self, name, start, 
    uid=None, end=None, start_date=None, end_date=None):
        #print(f"Event({uid}, {name}, {start}, {end})")
        self.name = name
        self.start = start

        if uid == None:
            self.uid = i_uid.get()
        else:
            self.uid = uid

        # Optional
        self.end = end
        self.start_date = start_date
        self.end_date = end_date
