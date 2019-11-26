commandDictionary = {}

def registerCommand(commandName, command):
    if commandName in commandDictionary:
        print(f"Command {commandName} already exists!")
    else:
        #print(f"Command {commandName} registered!")
        commandDictionary[commandName] = command

def findCommand(commandName):
    commandNameUpper = commandName.upper()
    return commandDictionary.get(commandNameUpper)

def executeCommand(commandName, args):
    foundCommand = findCommand(commandName)
    if foundCommand != None:
        return foundCommand.execute(args)
    else:
        return f"Could not find command {commandName}"
