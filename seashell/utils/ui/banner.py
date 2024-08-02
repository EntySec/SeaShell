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


class Banner(Config, Badges):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for
    providing tools for printing banners in UI.
    """

    def print_random_banner(self) -> None:
        """ Print random banner.

        :return None: None
        """

        if not os.path.exists(self.banners_path):
            self.print_warning("No banners detected.")
            return

        banners = list(os.listdir(self.banners_path))

        if not banners:
            self.print_warning("No banners detected.")
            return

        random_banner = random.randint(0, len(banners) - 1)
        banner = ColorScript().parse_file(
            self.banners_path + banners[random_banner]
        )

        self.set_less(False)
        self.print_empty(f"%newline%end{banner}%end%newline")
        self.set_less(True)
