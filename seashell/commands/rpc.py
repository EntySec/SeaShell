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
            'Options': [
                (
                    ('-L',),
                    {
                        'help': "Host to start RPC server on.",
                        'metavar': 'HOST',
                        'dest': 'host'
                    }
                ),
                (
                    ('-p', '--port'),
                    {
                        'help': "Port to start RPC server on.",
                        'metavar': 'PORT',
                        'type': int,
                        'required': True
                    }
                )
            ]
        })

        self.rpc = {}

    def run(self, args):
        if args.port in self.rpc:
            self.print_warning("RPC server is already running.")
            return

        self.rpc[args.port] = RPC(
            self.console, args.host or '0.0.0.0', args.port)
        self.rpc[args.port].run()
