#
# MIT License
#
# Copyright (c) 2020-2024 EntySec
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

APP_DIR      = Mussel.app
ARCHIVE      = $(APP_DIR).tar.gz
CONTENTS_DIR = $(APP_DIR)/Contents
INSTALL_DIR  = ../../seashell/data
IPA_FILE     = Mussel.zip
SYSROOT      = /Users/felix/Desktop/iOS-SDKs/iPhoneOS14.5.sdk

OBJS  = $(CONTENTS_DIR)/Info.plist $(CONTENTS_DIR)/MacOS/main
ARCHS = -arch arm64

CC     = clang
CFLAGS = $(ARCHS) -isysroot $(SYSROOT) -framework Foundation -lobjc -o

SIGN       = codesign
SIGN_FLAGS = -s EntySec --entitlements deps/sign.plist

HOST = 127.0.0.1
PORT = 8888

.PHONY: all clean app

all: $(OBJS)

$(CONTENTS_DIR)/MacOS/main: main.m
	$(CC) $(CFLAGS) $@ $<
	$(SIGN) $(SIGN_FLAGS) $@

$(CONTENTS_DIR)/Info.plist:
	python3 deps/plist.py $(HOST) $(PORT) $@

$(OBJS): | $(CONTENTS_DIR)

$(CONTENTS_DIR):
	mkdir -p $(CONTENTS_DIR)/MacOS

app: $(CONTENTS_DIR)
	tar -czvf $(ARCHIVE) $(APP_DIR)

install: $(OBJS)
	cp -r $(CONTENTS_DIR) $(INSTALL_DIR)

clean:
	rm -rf $(APP_DIR) $(ARCHIVE)