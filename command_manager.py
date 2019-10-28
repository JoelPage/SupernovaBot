import argparse as i_argparse

g_commandDictionary = {
}

def registerCommand(commandName, command):
    if commandName in g_commandDictionary:
        print(f"Command {commandName} already exists!")
    else:
        print(f"Registered Command {commandName}")
        g_commandDictionary[commandName] = command

def findCommand(commandName):
    # Handle command does not exist
    commandNameUpper = commandName.upper()
    return g_commandDictionary.get(commandNameUpper)

def executeCommand(commandName, args):
    try:
        findCommand(commandName).execute(args)
    except Exception as e:
        print(e)
