"""
MIT License

Copyright (c) 2020-2023 EntySec

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
import random

from colorscript import ColorScript

from badges import Badges

from seashell.lib.config import Config


class Tip(object):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for
    providing tools for printing tips in UI.
    """

    def __init__(self) -> None:
        super().__init__()

        self.config = Config()

        self.badges = Badges()
        self.color_script = ColorScript()

    def print_random_tip(self) -> None:
        """ Print random tip.

        :return None: None
        """

        if os.path.exists(self.config.tips_path):
            tips = []
            all_tips = os.listdir(self.config.tips_path)

            for tip in all_tips:
                tips.append(tip)

            if tips:
                tip = ""

                while not tip:
                    random_tip = random.randint(0, len(tips) - 1)
                    tip = self.color_script.parse_file(
                        self.config.tips_path + tips[random_tip]
                    )

                self.badges.print_empty(f"%newline%SeaShell Tip: {tip}%end%newline")
            else:
                self.badges.print_warning("No tips detected.")
        else:
            self.badges.print_warning("No tips detected.")
