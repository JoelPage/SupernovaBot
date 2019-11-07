import argparse as i_argparse

g_commandDictionary = {}

def registerCommand(commandName, command):
    if commandName in g_commandDictionary:
        print(f"Command {commandName} already exists!")
    else:
        #print(f"Registered Command {commandName}")
        g_commandDictionary[commandName] = command

def findCommand(commandName):
    # TODO : Handle command no exist
    commandNameUpper = commandName.upper()
    return g_commandDictionary.get(commandNameUpper)

def executeCommand(commandName, args):
    return findCommand(commandName).execute(args)
