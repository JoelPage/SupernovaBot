import uid

# Event Structure
# UID 
# Name 
# Description - Optional 
# Start Date Time - Optional 
# End Date Time  - Optional 
class Event(object):
    
    def __init__(self, name):
        self.uid = uid.get()
        self.name = name
      
#evnt = Event("test")
#print("Test Event :")
#print(evnt.uid)
#print(evnt.name)