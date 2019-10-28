import command_manager as i_command_manager
import argparse as i_argparse

class Command():
    requiredArgs = {}
    optionalArgs = {}

    def __init__(self, name):
        self.name = name
        i_command_manager.registerCommand(name, self)

    def getNumArgs(self):
        return self.getNumRequiredArgs() + self.getNumOptionalArgs()

    def getNumRequiredArgs(self):
        return len(self.requiredArgs)

    def getNumOptionalArgs(self):
        return len(self.optionalArgs)

    def execute(self, args):
        return self.parseArgs(args)

    def parseArgs(self, args):
        parser = i_argparse.ArgumentParser(f"{self.name}")
        for arg in self.requiredArgs:
            parser.add_argument(arg.name, type=arg.type, help=arg.help)
        for arg in self.optionalArgs:
            parser.add_argument(f"-{arg.name}", type=arg.type, help=arg.help)
        return parser.parse_args(args)

class Argument():
    def __init__(self, name, type=None, help=None, nargs=None):
        self.name = name
        self.type = type
        self.help = help
        self.nargs = nargs