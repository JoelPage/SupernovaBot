print("snCommands/command.py")
# Python
import argparse
# Supernova Commands
import snCommands.manager as manager

class Command():
    requiredArgs = {}
    optionalArgs = {}
    subCommands = []

    def __init__(self, name):
        self.name = name
        manager.registerCommand(name, self)

    def execute(self, args):
        try:
            parsedArgs = self.parseArgs(args)
            print("Arguments parsed")
            for subCommand in self.subCommands:
                print(f"{subCommand.name} == {parsedArgs.subname}")
                if subCommand.name == parsedArgs.subname:
                    value = subCommand.executeInternal(parsedArgs) 
                    print("Subcommand executed")
                    return Result(value=value)
            value = self.executeInternal(parsedArgs)
            print("Command executed")
            return Result(value=value)
        except Exception as e:
            print("Command exception raised")
            return Result(error=e.args[0])

    def executeInternal(self, args):
        return "Function executeInternal not overriden!"

    def parseArgs(self, args):
        try:
            parser = argparse.ArgumentParser(f"{self.name}")
            for arg in self.requiredArgs:
                parser.add_argument(arg.name, type=arg.type, help=arg.help, choices=arg.choices)
            for arg in self.optionalArgs:
                parser.add_argument(f"-{arg.name}", type=arg.type, help=arg.help, choices=arg.choices)
            if len(self.subCommands) > 0:
                subparsers = parser.add_subparsers(dest="subname")
                for subCommand in self.subCommands:
                    subCommand.addToParser(subparsers)
            return parser.parse_args(args)
        except ValueError as ve:
            print("ValueError raised")
            raise Exception(f"{ve.args}, Review the Usage {parser.format.usage()}")
        except argparse.ArgumentError as ae:
            print("argparse.ArgumentError raised")
            raise Exception(f"{ae.args}, Review the Usage: {parser.format_usage()}")
        except SystemExit as ex:
            print("SystemExit raised")
            if ex.args[0] == 0:
                raise Exception(f"You requested some help! Here you go:\n{parser.format_help()}")
            else:
                raise Exception(f"Something went wrong! Review the Usage:\n{parser.format_usage()}")

    def addToParser(self, subparsers):
        parser = subparsers.add_parser(self.name)
        for arg in self.requiredArgs:
            parser.add_argument(arg.name, type=arg.type, help=arg.help, choices=arg.choices)
        for arg in self.optionalArgs:
            parser.add_argument(f"-{arg.name}", type=arg.type, help=arg.help, choices=arg.choices)
        if len(self.subCommands) > 0:
            subparsers = parser.add_subparsers(dest="subname")
            for subCommand in self.subCommands:
                subCommand.addToParser(subparsers)
            
class Argument():
    def __init__(self, name, type=None, help=None, choices=None, nargs=None):
        self.name = name
        self.type = type
        self.help = help
        self.choices = choices
        self.nargs = nargs

class Result():
    def __init__(self, error=None, value=None):
        self.value = value
        self.error = error