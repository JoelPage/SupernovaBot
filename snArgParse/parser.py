print("snArgParse/parser.py")
# Python
import argparse
import sys

class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print("This is an overrided error function")
        print(f"{message}")
        self.print_help(sys.stderr)
        self.exit(2, '%s: error: %s\n' % (self.prog, message))

    def exit(self, status=0, message=None):
        if status:
            raise Exception(message)
        exit(status)