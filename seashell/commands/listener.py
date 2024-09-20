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
from hatsploit.lib.ui.jobs import Job


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "listener",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Manage TCP listener.",
            'Options': [
                (
                    ('-L',),
                    {
                        'help': "Host to start TCP listener on.",
                        'metavar': 'HOST',
                        'dest': 'host'
                    }
                ),
                (
                    ('-p', '--port'),
                    {
                        'help': "Port to start TCP listener on.",
                        'metavar': 'PORT',
                        'type': int,
                        'required': True
                    }
                ),
                (
                    ('-k', '--kill'),
                    {
                        'help': "Kill running TCP listener.",
                        'action': 'store_true'
                    }
                )
            ]
        })

        self.hint = False
        self.jobs = {}

    def handle_device(self, handler, job) -> None:
        handler.start()

        def shutdown_submethod(handler):
            self.print_process("Terminating TCP handler...")

            try:
                handler.stop()
            except RuntimeError:
                return

        job.set_exit(target=shutdown_submethod, args=(handler,))

        while True:
            device = handler.handle()

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
                    f"Type %greendevices -i {str(len(self.console.devices) - 1)}%end "
                    "to interact this device."
                )
                self.hint = True

    def run(self, args):
        if args.kill:
            if args.port not in self.jobs:
                self.print_error(f"No TCP listener running on port {str(args.port)}!")
                return

            self.print_process(f"Killing TCP listener on port {str(args.port)}...")

            self.jobs[args.port].shutdown()
            self.jobs[args.port].join()
            self.jobs.pop(args.port)

            return

        if args.port in self.jobs:
            self.print_warning("TCP listener is already running.")
            return

        handler = DeviceHandler(
            args.host or '0.0.0.0', args.port, None)

        job = Job(target=self.handle_device, args=(handler,))
        job.pass_job = True
        job.start()

        self.jobs.update({args.port: job})
        self.print_information(
            f"Use %greenlistener -p {str(args.port)} -k%end to stop.")
