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
import random

from colorscript import ColorScript

from badges import Badges

from seashell.lib.config import Config


class Tip(Config, Badges):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for
    providing tools for printing tips in UI.
    """

    def print_random_tip(self) -> None:
        """ Print random tip.

        :return None: None
        """

        if not os.path.exists(self.tips_path):
            self.print_warning("No tips detected.")
            return

        tips = list(os.listdir(self.tips_path))

        if not tips:
            self.print_warning("No tips detected.")
            return

        random_tip = random.randint(0, len(tips) - 1)
        tip = ColorScript().parse_file(
            self.tips_path + tips[random_tip]
        )

        self.print_empty(f"%newline%endSeaShell Tip: {tip}%end%newline")
