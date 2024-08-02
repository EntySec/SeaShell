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

from badges.cmd import Cmd

from seashell.utils.ui.banner import Banner
from seashell.utils.ui.tip import Tip

from seashell.lib.config import Config


class Console(Cmd):
    """ Subclass of seashell.core module.

    This subclass of seashell.core modules is intended for providing
    main SeaShell Framework console interface.
    """

    def __init__(self) -> None:
        self.config = Config()
        self.config.setup()

        super().__init__(
            prompt='(%lineseashell%end)> ',
            path=[self.config.commands_path],
            history=self.config.history_path,
            console=self
        )

        self.devices = {}
        self.version = '1.0.0'

    def do_exit(self, _) -> None:
        """ Exit SeaShell Framework.

        :return None: None
        :raises EOFError: EOF error
        """

        for device in list(self.devices):
            self.devices[device]['device'].kill()
            del self.devices[device]

        raise EOFError

    def do_tip(self, _) -> None:
        """ Print random tip.

        :return None: None
        """

        Tip().print_random_tip()

    def do_banner(self, _) -> None:
        """ Print random banner.

        :return None: None
        """

        Banner().print_random_banner()

    def console(self) -> None:
        """ Start SeaShell console.

        :return None: None
        """

        modules = 0
        plugins = 0

        if os.path.exists(self.config.modules_path):
            for _, _, files in os.walk(self.config.modules_path):
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        modules += 1

        if os.path.exists(self.config.plugins_path):
            for _, _, files in os.walk(self.config.plugins_path):
                for file in files:
                    if file.endswith('.py') and file != '__init__.py':
                        plugins += 1

        header = ""
        header += "%end"
        header += f"   --=[ %bold%whiteSeaShell Framework {self.version}%end%newline"
        header += "--==--[ Developed by EntySec (%linehttps://entysec.com/%end)%newline"
        header += f"   --=[ %green{str(modules)}%end modules | %green{str(plugins)}%end plugins"
        header += "%end"

        self.print_empty('%clear', end='')

        Banner().print_random_banner()
        self.print_empty(header)
        Tip().print_random_tip()

        self.loop()
