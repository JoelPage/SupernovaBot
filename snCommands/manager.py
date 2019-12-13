print("snCommands/manager.py")
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
    # Replace italicised quotes with regular quotes before parsing args.
    print(args)
    for arg in args:
        arg.replace('”', '"')
        arg.replace('“', '"')
    print(args)
    foundCommand = findCommand(commandName)
    if foundCommand != None:
        return foundCommand.execute(args)
    else:
        return f"Could not find command {commandName}"
