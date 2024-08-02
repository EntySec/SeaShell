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
import datetime

from badges import Badges
from typing import Optional, Union

from pex.fs import FS
from pex.string import String

from seashell.lib.config import Config


class Loot(Config, Badges, String, FS):
    """ Subclass of seashell.lib module.

    This subclass of seashell.lib module is intended for providing
    tools for working with loot collected by SeaShell.
    """

    def create_loot(self) -> None:
        """ Create loot directory in workspace.

        :return None: None
        """

        if not os.path.isdir(self.loot_path):
            os.mkdir(self.loot_path)

    def specific_loot(self, filename: str) -> str:
        """ Return full path to the specific file
        from the loot directory.

        :param str filename: file name
        :return str: path to the file
        """

        return self.loot_path + filename

    def random_loot(self, extension: Optional[str] = None) -> str:
        """ Generate random loot path and add extension (if specified).

        :param Optional[str] extension: extension
        :return str: random loot path
        """

        filename = self.random_string(16)

        if extension:
            filename += '.' + extension

        return self.loot_path + filename

    def get_file(self, filename: str) -> bytes:
        """ Get specific file contents.

        :param str filename: file name
        :return bytes: file contents
        """

        self.check_file(filename)

        with open(filename, 'rb') as f:
            return f.read()

    def save_file(self, location: str, data: bytes, extension: Optional[str] = None,
                  filename: Optional[str] = None) -> Union[str, None]:
        """ Save contents to specific location.

        :param str location: location
        :param bytes data: contents to save
        :param Optional[str] extension: file extension
        :param Optional[str] filename: file name
        :return Union[str, None]: path if success else None
        """

        exists, is_dir = self.exists(location)

        if exists:
            if is_dir:
                if location.endswith('/'):
                    location += os.path.split(filename)[1] if filename else self.random_string(16)
                else:
                    location += '/' + os.path.split(filename)[1] if filename else self.random_string(16)

            if extension:
                if not location.endswith('.' + extension):
                    location += '.' + extension

            with open(location, 'wb') as f:
                f.write(data)

            self.print_success(f"Saved to {location}!")
            return os.path.abspath(location)

        return None

    def remove_file(self, filename: str) -> None:
        """ Remove specific file.

        :param str filename: file name
        :return None: None
        """

        self.check_file(filename)
        os.remove(filename)

        self.badges.print_success(f"Removed {filename}!")

    def get_loot(self, filename: str) -> bytes:
        """ Get specific loot contents.

        :param str filename: file name of loot
        :return bytes data: loot contents
        """

        filename = os.path.split(filename)[1]
        return self.get_file(self.loot_path + filename)

    def save_loot(self, filename: str, data: bytes) -> Union[str, None]:
        """ Save contents to loot directory.

        :param str filename: file name of loot
        :param bytes data: loot contents
        :return Union[str, None]: path if success else None
        """

        filename = os.path.split(filename)[1]
        return self.save_file(self.loot_path + filename, data)

    def remove_loot(self, filename: str) -> None:
        """ Remove specific loot from loot directory.

        :param str filename: file name of loot
        :return None: None
        """

        filename = os.path.split(filename)[1]
        self.remove_file(self.loot_path + filename)

    def get_data(self, filename: str) -> bytes:
        """ Get contents of file from data directory.

        :param str filename: file name
        :return bytes: data contents
        :raises RuntimeError: with trailing error message
        """

        if os.path.exists(self.data_path + filename):
            with open(self.data_path + filename, 'rb') as f:
                return f.read()
        else:
            raise RuntimeError("Invalid data given!")

    def list_loot(self) -> list:
        """ List all loots from loot directory.

        :return list: all loots from loot directory
        """

        loots = []

        for loot in os.listdir(self.loot_path):
            loots.append((loot, self.loot_path + loot, datetime.datetime.fromtimestamp(
                os.path.getmtime(self.loot_path + loot)).astimezone().strftime(
                "%Y-%m-%d %H:%M:%S %Z")))

        return loots
