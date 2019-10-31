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
    try:
        return findCommand(commandName).execute(args)
    except i_argparse.ArgumentError as e: 
        print(e)
    except i_argparse.ArgumentTypeError as e:
        print(e)
    except Exception as e:
        print(e)
    except:
        print("Unhandled Exception")
