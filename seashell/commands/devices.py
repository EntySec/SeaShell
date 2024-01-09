"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "manage",
            'Name': "devices",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Manage connected devices.",
            'Usage': "devices <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                '-l': ['', 'List connected devices.'],
                '-k': ['<id>', 'Kill device by ID.'],
                '-i': ['<id>', 'Interact device by ID.'],
            }
        }

    def rpc(self, *args):
        if len(args) < 1:
            return

        if args[0] == 'list':
            return self.console.devices

        if args[0] == 'kill':
            return self.run(3, [self.details['Name'], '-k', args[1]])

    def run(self, argc, argv):
        if argv[1] == '-l':
            if not self.console.devices:
                self.print_warning("No devices connected.")
                return

            devices = []

            for device in self.console.devices:
                devices.append(
                    (device, self.console.devices[device]['host'],
                        self.console.devices[device]['port']))

            self.print_table("Connected Devices", ('ID', 'Host', 'Port'), *devices)

        elif argv[1] == '-k':
            device_id = int(argv[2])

            if device_id not in self.console.devices:
                self.print_error("Invalid device ID!")
                return

            self.console.devices[device_id]['device'].kill()
            self.console.devices.pop(device_id)

        elif argv[1] == '-i':
            device_id = int(argv[2])

            if device_id not in self.console.devices:
                self.print_error("Invalid device ID!")
                return

            self.print_process(f"Interacting with device {str(device_id)}...")

            self.console.prompt_fill = \
                self.console.devices[device_id]['device'].device.prompt
            self.console.devices[device_id]['device'].interact()
            self.console.prompt_fill = self.console.prompt
