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
            for subCommand in self.subCommands:
                if subCommand.name == parsedArgs.subname:
                    return subCommand.executeInternal(parsedArgs)
            return self.executeInternal(parsedArgs)
        except Exception as e:
            return Result(error=e.args[0])

    def executeInternal(self, args):
        return Result(value="Function executeInternal not overrided!")

    def parseArgs(self, args):
        try:
            parser = argparse.ArgumentParser(f"{self.name}")
            print(f"Create Arg Parser {self.name}")
            for arg in self.requiredArgs:
                print(f"Adding Required Arg {arg.name} to {self.name}")
                parser.add_argument(arg.name, type=arg.type, help=arg.help, choices=arg.choices)
            for arg in self.optionalArgs:
                print(f"Adding Optional Arg -{arg.name} to {self.name}")
                parser.add_argument(f"-{arg.name}", type=arg.type, help=arg.help, choices=arg.choices)
            if len(self.subCommands) > 0:
                subparsers = parser.add_subparsers(dest="subname")
                for subCommand in self.subCommands:
                    print(f"Adding Sub Command {subCommand.name} to {self.name}")
                    subCommand.addToParser(subparsers)
            return parser.parse_args(args)
        except ValueError as ve:
            raise Exception(f"{ve.args}, Review the Usage {parser.format.usage()}")
        except argparse.ArgumentError as ae:
            raise Exception(f"{ae.args}, Review the Usage: {parser.format_usage()}")
        except SystemExit as ex:
            if ex.args[0] == 0:
                raise Exception(f"You requested some help! Here you go:\n{parser.format_help()}")
            else:
                raise Exception(f"Something went wrong! Review the Usage:\n{parser.format_usage()}")

    def addToParser(self, subparsers):
        parser = subparsers.add_parser(self.name)
        for arg in self.requiredArgs:
            print(f"Adding Required Arg {arg.name} to {self.name}")
            parser.add_argument(arg.name, type=arg.type, help=arg.help, choices=arg.choices)
        for arg in self.optionalArgs:
            print(f"Adding Optional Arg -{arg.name} to {self.name}")
            parser.add_argument(f"-{arg.name}", type=arg.type, help=arg.help, choices=arg.choices)
        if len(self.subCommands) > 0:
            subparsers = parser.add_subparsers(dest="subname")
            for subCommand in self.subCommands:
                print(f"Adding Sub Command {subCommand.name} to {self.name}")
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