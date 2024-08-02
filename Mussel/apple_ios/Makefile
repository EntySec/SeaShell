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

APP_DIR     = Mussel.app
INSTALL_DIR = ../../seashell/data
IPA_FILE    = Mussel.ipa

OBJS  = $(addprefix $(APP_DIR)/,main Info.plist)
ARCHS = -arch arm64

CC     = clang
CFLAGS = $(ARCHS) -isysroot $(SDK) -framework Foundation -framework UIKit -lobjc -o

SIGN       = ldid
SIGN_FLAGS = -Sdeps/sign.plist

HOST = 127.0.0.1
PORT = 8888

.PHONY: all clean ipa

all: $(OBJS)

$(APP_DIR)/main: main.m
	$(CC) $(CFLAGS) $@ $<
	$(SIGN) $(SIGN_FLAGS) $@

$(APP_DIR)/Info.plist:
	python3 deps/plist.py $(HOST) $(PORT) $(APP_DIR)/Info.plist

$(OBJS): | $(APP_DIR)

$(APP_DIR):
	mkdir -p $(APP_DIR)

install: $(OBJS)
	cp -r $(APP_DIR) $(INSTALL_DIR)

hook: hook.m
	$(CC) $(CFLAGS) -o $@ $<
	$(SIGN) $(SIGN_FLAGS) $@
	ct_bypass -i $@ -o $@ -r

ipa: $(APP_DIR)
	mkdir Payload
	cp -r $(APP_DIR) Payload/
	zip -r $(IPA_FILE) Payload/
	rm -rf Payload/

clean:
	rm -rf $(APP_DIR) $(IPA_FILE)