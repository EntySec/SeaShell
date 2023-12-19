#
# MIT License
#
# Copyright (c) 2020-2023 EntySec
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

APP_DIR  = Mussel.app
IPA_FILE = Mussel.ipa
SYSROOT  = /Users/felix/Desktop/iOS-SDKs/iPhoneOS14.5.sdk

OBJS  = $(addprefix $(APP_DIR)/,main Info.plist)
ARCHS = -arch arm64 -arch arm64e

.PHONY: all mussel clean ipa

all: $(OBJS) $(TARGET) ipa

$(APP_DIR)/main: main.m
	clang $(ARCHS) -isysroot $(SYSROOT) -framework Foundation -framework UIKit -lobjc -o $@ $<
	ldid -Sdeps/sign.plist $@

$(APP_DIR)/mussel: mussel.m
	clang $(ARCHS) -isysroot $(SYSROOT) -framework Foundation -framework UIKit -lobjc -o $@ $<

$(APP_DIR)/Info.plist:
	python3 deps/plist.py 127.0.0.1 8888 $(APP_DIR)/Info.plist

$(OBJS): | $(APP_DIR)

$(APP_DIR):
	mkdir -p $(APP_DIR)

ipa:
	mkdir Payload
	cp -r $(APP_DIR) Payload/
	zip -r $(IPA_FILE) Payload/
	rm -rf Payload/

clean:
	rm -rf $(APP_DIR) $(IPA_FILE)

