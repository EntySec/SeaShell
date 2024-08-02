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
import pathlib


class Config(object):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for providing
    basic configuration for SeaShell.
    """

    user_path = f'{pathlib.Path.home()}/.seashell/'
    base_path = f'{os.path.dirname(os.path.dirname(__file__))}/'
    data_path = base_path + 'data/'

    banners_path = data_path + 'banners/'
    tips_path = data_path + 'tips/'

    modules_path = base_path + 'modules/'
    plugins_path = base_path + 'plugins/'
    commands_path = base_path + 'commands/'

    loot_path = user_path + 'loot/'
    history_path = user_path + 'history.txt'

    def setup(self) -> None:
        """ Setup config and create paths.

        :return None: None
        """

        if not os.path.exists(self.user_path):
            os.mkdir(self.user_path)

        if not os.path.exists(self.loot_path):
            os.mkdir(self.loot_path)
