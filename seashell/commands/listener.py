"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

import ctypes
import threading

from seashell.core.device import (
    Device,
    DeviceHandler
)

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "listener",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Manage TCP listener.",
            'Usage': "listener <option> <arguments>",
            'MinArgs': 1,
            'Options': {
                'on': ['<host> <port>', 'Start TCP listener.'],
                'off': ['', 'Stop TCP listener.']
            }
        })

        self.hint = False
        self.handler = None
        self.thread = None

    def handle_device(self) -> None:
        """ Thread to handle devices.

        :return None: None
        """

        while True:
            device = self.handler.handle()

            self.console.devices.update({
                len(self.console.devices): {
                    'host': device.client[0],
                    'port': str(device.client[1]),
                    'platform': str(device.platform),
                    'device': device
                }
            })

            if not self.hint:
                self.print_information(
                    f"Type %greendevices list%end to list all connected devices.")
                self.print_information(
                    f"Type %greendevices interact {str(len(self.console.devices) - 1)}%end "
                    "to interact this device."
                )
                self.hint = True

    def rpc(self, *args):
        if len(args) < 1:
            return

        if args[0] == 'off':
            return self.run([self.info['Name'], 'off'])

        if args[0] == 'on':
            if len(args) < 3:
                return

            return self.run([self.info['Name'], 'on', args[1], args[2]])

    def run(self, args):
        if args[1] == 'on':
            if self.handler:
                self.print_warning("TCP listener is already running.")
                return

            self.handler = DeviceHandler(args[2], args[3], None)
            self.handler.start()

            self.thread = threading.Thread(target=self.handle_device)
            self.thread.setDaemon(True)
            self.thread.start()

            self.print_information("Use %greenlistener off%end to stop.")

        elif args[1] == 'off':
            if not self.handler:
                self.print_warning("TCP listener is not started.")
                return

            if self.thread.is_alive:
                exc = ctypes.py_object(SystemExit)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.thread.ident), exc)

                if res > 1:
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(self.thread.ident, None)
                    self.print_error("Failed to stop listener!")
                    return

            self.thread = None
            self.handler = None
