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
            'Usage': "devices <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'list': ['', 'List connected devices.'],
                'kill': ['<id>', 'Kill device by ID.'],
                'interact': ['<id>', 'Interact device by ID.'],
            }
        })

    def rpc(self, *args):
        if len(args) < 1:
            return

        if args[0] == 'list':
            return self.console.devices

        if args[0] == 'kill':
            return self.run([self.info['Name'], 'kill', args[1]])

    def run(self, args):
        if args[1] == 'list':
            if not self.console.devices:
                self.print_warning("No devices connected.")
                return

            devices = []

            for device in self.console.devices:
                info = self.console.devices[device]

                devices.append(
                    (device, info['host'], info['port'], info['platform']))

            self.print_table("Connected Devices", ('ID', 'Host', 'Port', 'Platform'), *devices)

        elif args[1] == 'kill':
            device_id = int(args[2])

            if device_id not in self.console.devices:
                self.print_error("Invalid device ID!")
                return

            self.console.devices[device_id]['device'].kill()
            self.console.devices.pop(device_id)

        elif args[1] == 'interact':
            device_id = int(args[2])

            if device_id not in self.console.devices:
                self.print_error("Invalid device ID!")
                return

            self.print_process(f"Interacting with device {str(device_id)}...")
            self.console.devices[device_id]['device'].interact()
