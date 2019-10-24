class argumentData(object):
    def __init__(self, mask, func):
        self.mask = mask
        self.func = func

def handleArgDate(event, mask, args):
    weather = args[0]

    #throwException(parseWeather(args))

    event.weather = weather 
    recursiveFunction(event, mask, args[2:])
    return

def handleArgToday(event, mask, args):
    return

def handleArgStartDate(event, mask, args):
    
    return

def handleArgEndDate(event, mask, args):
    return

def handleArgRepeat(event, mask, args):
    return

def handleArgExpire(event, mask, args):
    return

def handleArgDesc(event, mask, args):
    return

def commandArgData(arg):
    argU = arg.upper()
    switch = {
    "DATE" : argumentData(1 << 0, handleArgDate, parseDate),               # Set Start and End Date
    "TODAY" : argumentData(1 << 1, handleArgToday, parseDate),             # Set Start and End Date as Today's Date
    "START-DATE" : argumentData(1 << 2, handleArgStartDate),    # Set Start Date
    "END-DATE" : argumentData(1 << 3, handleArgEndDate),        # Set End Date
    "REPEAT" : argumentData(1 << 4, handleArgRepeat),           # Set the Days of the week this event will Repeat
    "EXPIRE" : argumentData(1 << 5, handleArgExpire),           # Set the date this event will Stop repeating
    "DESC" : argumentData(1 << 6, handleArgDesc),               # Set the event Description
    "DESCRIPTION" : argumentData(1 << 6, handleArgDesc)         # Set the event Description
    }
    return switch.get(argU)

event = None

args = { "date", "21/1", "end-date", "21/2", "repeat", "Thu, Sun, Mon" }
    
argumentsMask = 0

for arg in args:
    argData = commandArgData(args[0])
    if argumentsMask & argData.mask:
        print(f"Argument [{arg}] already processed.")
        # Exit Commands or Attempt to continue ?
        # Continue sounds risky when they can !edit <args> with a correctly formed command.
    else:
        argumentsMask |= argData.mask
        argData.func(event, argumentsMask, args[1:])