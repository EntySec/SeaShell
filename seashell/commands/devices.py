"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "devices",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Manage connected devices.",
            'MinArgs': 1,
            'Options': [
                (
                    ('-l', '--list'),
                    {
                        'help': "List connected devices.",
                        'action': 'store_true'
                    }
                ),
                (
                    ('-k', '--kill'),
                    {
                        'help': "Kill connected device by ID.",
                        'metavar': 'ID',
                        'type': int
                    }
                ),
                (
                    ('-i', '--interact'),
                    {
                        'help': "Interact connected device by ID.",
                        'metavar': 'ID',
                        'type': int
                    }
                )
            ],
        })

    def rpc(self, *args):
        if len(args) < 1:
            return

        if args[0] == 'list':
            return self.console.devices

        if args[0] == 'kill':
            return self.run([self.info['Name'], 'kill', args[1]])

    def run(self, args):
        if args.list:
            if not self.console.devices:
                self.print_warning("No devices connected.")
                return

            devices = []

            for device in self.console.devices:
                info = self.console.devices[device]

                devices.append(
                    (device, info['host'], info['port'], info['platform']))

            self.print_table("Connected Devices",
                             ('ID', 'Host', 'Port', 'Platform'), *devices)

        elif args.kill is not None:
            if args.kill not in self.console.devices:
                self.print_error("Invalid device ID!")
                return

            self.console.devices[args.kill]['device'].kill()
            self.console.devices.pop(args.kill)

        elif args.interact is not None:
            if args.interact not in self.console.devices:
                self.print_error("Invalid device ID!")
                return

            self.print_process(
                f"Interacting with device {str(args.interact)}...")
            self.console.devices[args.interact]['device'].interact()
