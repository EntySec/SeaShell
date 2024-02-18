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

from pwny.api import *
from pwny.types import *

GATHER_BASE = 9

GATHER_GET_INFO = tlv_custom_tag(API_CALL_STATIC, GATHER_BASE, API_CALL)

GATHER_NAME = tlv_custom_type(TLV_TYPE_STRING, GATHER_BASE, API_TYPE)
GATHER_OS = tlv_custom_type(TLV_TYPE_STRING, GATHER_BASE, API_TYPE + 1)
GATHER_MODEL = tlv_custom_type(TLV_TYPE_STRING, GATHER_BASE, API_TYPE + 2)
GATHER_SERIAL = tlv_custom_type(TLV_TYPE_STRING, GATHER_BASE, API_TYPE + 3)
GATHER_UDID = tlv_custom_type(TLV_TYPE_STRING, GATHER_BASE, API_TYPE + 4)

LOCATE_BASE = 8

LOCATE_GET = tlv_custom_tag(API_CALL_STATIC, LOCATE_BASE, API_CALL)

LOCATE_LONGITUDE = tlv_custom_type(TLV_TYPE_STRING, LOCATE_BASE, API_TYPE)
LOCATE_LATITUDE = tlv_custom_type(TLV_TYPE_STRING, LOCATE_BASE, API_TYPE + 1)
