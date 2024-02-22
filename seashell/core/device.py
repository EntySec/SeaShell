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

from pex.arch.types import *
from pex.platform.types import *
from pex.proto.tcp import TCPListener

from pwny.session import PwnySession

from typing import Tuple
from badges import Badges

from seashell.lib.config import Config
from seashell.core.api import *


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

        self.config = Config()

        self.badges = Badges()
        self.device = session

        self.uuid = session.uuid
        self.host = session.details['Host']
        self.port = session.details['Port']

        self.name = None
        self.os = None
        self.model = None
        self.serial = None
        self.udid = None

    def update_details(self) -> None:
        """ Update device details.

        :return None: None
        """

        result = self.device.send_command(tag=GATHER_GET_INFO)

        self.name = result.get_string(GATHER_NAME)
        self.os = result.get_string(GATHER_OS)
        self.model = result.get_string(GATHER_MODEL)
        self.serial = result.get_string(GATHER_SERIAL)
        self.udid = result.get_string(GATHER_UDID)

    def locate(self) -> Tuple[str, str]:
        """ Get device current latitude and longitude.

        :return Tuple[str, str]: tuple of latitude and longitude
        """

        result = self.device.send_command(tag=LOCATE_GET)

        return result.get_string(LOCATE_LATITUDE), \
            result.get_string(LOCATE_LONGITUDE)

    def kill(self) -> None:
        """ Disconnect the specified device.

        :return None: None
        """

        self.device.close()

    def interact(self) -> None:
        """ Interact with the specified device.

        :return None: None
        """

        self.badges.print_process("Loading additional bundles...")

        self.device.load_commands(self.config.modules_path)
        self.device.load_plugins(self.config.plugins_path)

        self.badges.print_success("Interactive connection spawned!")
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
            f"New device connected - {self.address[0]}!")

        return Device(session)
