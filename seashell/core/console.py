"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import cmd
import sys

from badges import Badges, Tables
from colorscript import ColorScript

from hatsploit.lib.commands import Commands
from hatsploit.lib.runtime import Runtime

from seashell.utils.ui.banner import Banner
from seashell.utils.ui.tip import Tip

from seashell.lib.config import Config


class Console(cmd.Cmd):
    """ Subclass of seashell.core module.

    This subclass of seashell.core modules is intended for providing
    main SeaShell Framework console interface.
    """

    def __init__(self) -> None:
        super().__init__()
        cmd.Cmd.__init__(self)

        self.badges = Badges()
        self.tables = Tables()

        self.banner = Banner()
        self.tip = Tip()
        self.config = Config()

        self.commands = Commands()
        self.runtime = Runtime()

        self.config.setup()

        self.core_commands = sorted([
            ('clear', 'Clear terminal window.'),
            ('exit', 'Exit SeaShell Framework.'),
            ('help', 'Show available commands.'),
            ('banner', 'Print random banner.'),
            ('tip', 'Print random tip.'),
        ])
        self.custom_commands = {}

        self.devices = {}
        self.prompt = ColorScript().parse_input(
            f'%remove(%lineseashell%end)> ')
        self.prompt_fill = self.prompt
        self.version = '1.0.0'

    def do_help(self, _) -> None:
        """ Show available commands.

        :return None: None
        """

        self.tables.print_table("Core Commands", ('Command', 'Description'), *self.core_commands)
        self.commands.show_commands(self.custom_commands)

    def do_exit(self, _) -> None:
        """ Exit SeaShell Framework.

        :return None: None
        :raises EOFError: EOF error
        """

        for device in list(self.devices):
            self.devices[device]['device'].kill()
            del self.devices[device]

        raise EOFError

    def do_clear(self, _) -> None:
        """ Clear terminal window.

        :return None: None
        """

        self.badges.print_empty('%clear', end='')

    def do_tip(self, _) -> None:
        """ Print random tip.

        :return None: None
        """

        self.tip.print_random_tip()

    def do_banner(self, _) -> None:
        """ Print random banner.

        :return None: None
        """

        self.banner.print_random_banner()

    def do_EOF(self, _):
        """ Catch EOF.

        :return None: None
        :raises EOFError: EOF error
        """

        raise EOFError

    def default(self, line: str) -> None:
        """ Default unrecognized command handler.

        :param str line: line sent
        :return None: None
        """

        command = line.split()
        self.commands.execute_custom_command(command, self.custom_commands)

    def emptyline(self) -> None:
        """ Do something on empty line.

        :return None: None
        """

        pass

    def load_commands(self) -> None:
        """ Load custom SeaShell commands.

        :return None: None
        """

        self.custom_commands.update(
            self.commands.load_commands(self.config.commands_path))

        for command in self.custom_commands:
            self.custom_commands[command].console = self

    def console(self) -> None:
        """ Start SeaShell console.

        :return None: None
        """

        modules = 0
        plugins = 0

        if os.path.exists(self.config.modules_path):
            for module in os.listdir(self.config.modules_path):
                if module.endswith('.py'):
                    modules += 1

        if os.path.exists(self.config.plugins_path):
            for plugin in os.listdir(self.config.plugins_path):
                if plugin.endswith('.py'):
                    plugins += 1

        header = ""
        header += "%end"
        header += f"   --=[ %bold%whiteSeaShell Framework {self.version}%end%newline"
        header += "--==--[ Developed by EntySec (%linehttps://entysec.com/%end)%newline"
        header += f"   --=[ %green{str(modules)}%end modules | %green{str(plugins)}%end plugins"
        header += "%end"

        self.badges.print_empty('%clear', end='')
        self.banner.print_random_banner()
        self.badges.print_empty(header)

        self.tip.print_random_tip()
        self.load_commands()

        while True:
            result = self.runtime.catch(self.shell)

            if result is not Exception and result:
                break

    def shell(self) -> bool:
        """ Run console shell.

        :return bool: True to exit
        """

        try:
            cmd.Cmd.cmdloop(self)

        except (EOFError, KeyboardInterrupt):
            self.badges.print_empty(end='')
            return True

        return False
