"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from seashell.utils.rpc import RPC

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "rpc",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Manage RPC server.",
            'Usage': "rpc <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'on': ['<host> <port>', 'Turn RPC server on.'],
                'off': ['', 'Turn RPC server off.'],
            }
        })

        self.rpc = None

    def run(self, args):
        if args[1] == 'on':
            if self.rpc:
                self.print_warning("RPC server is already running.")
                return

            self.rpc = RPC(self.console, args[2], args[3])
            self.rpc.run()

        elif args[1] == 'off':
            if not self.rpc:
                self.print_warning("RPC server is not running.")
                return
