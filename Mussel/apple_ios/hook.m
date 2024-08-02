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

#include <spawn.h>
#include <mach-o/dyld.h>
#include <sys/sysctl.h>
#include <unistd.h>

#ifdef DEBUG
#define NSLog(...) NSLog(__VA_ARGS__)
#else
#define NSLog(...) NULL
#endif

#define POSIX_SPAWN_PERSONA_FLAGS_OVERRIDE 1
extern int posix_spawnattr_set_persona_np(const posix_spawnattr_t* __restrict, uid_t, uint32_t);
extern int posix_spawnattr_set_persona_uid_np(const posix_spawnattr_t* __restrict, uid_t);
extern int posix_spawnattr_set_persona_gid_np(const posix_spawnattr_t* __restrict, uid_t);

BOOL spawnProcess(NSString *path, NSArray *args)
{
    NSMutableArray *argsMutable;

    NSUInteger iter;
    NSUInteger argsCount;

    NSMutableString *stdoutString;
    NSMutableString *stderrString;

    int status;
    char **argv;

    pid_t taskPid;

    posix_spawnattr_t attr;

    argsMutable = args.mutableCopy ? : [NSMutableArray new];
    [argsMutable insertObject:path atIndex:0];

    argsCount = [argsMutable count];
    argv = (char **)malloc((argsCount + 1) * sizeof(char *));

    for (iter = 0; iter < argsCount; iter++)
    {
        argv[iter] = strdup([[argsMutable objectAtIndex:iter] UTF8String]);
    }

    argv[argsCount] = NULL;

    posix_spawnattr_init(&attr);
    posix_spawnattr_set_persona_np(&attr, 99, POSIX_SPAWN_PERSONA_FLAGS_OVERRIDE);
    posix_spawnattr_set_persona_uid_np(&attr, 0);
    posix_spawnattr_set_persona_gid_np(&attr, 0);
    posix_spawnattr_setflags(&attr, POSIX_SPAWN_SETPGROUP);

    status = posix_spawn(&taskPid, [path UTF8String], NULL, &attr, (char* const*)argv, NULL);
    posix_spawnattr_destroy(&attr);

    for (iter = 0; iter < argsCount; iter++)
    {
        free(argv[iter]);
    }

    free(argv);

    if (status != 0)
    {
        NSLog(@"[%s] Operation failed, posix_spawn error %d\n", __PRETTY_FUNCTION__, status);
        return NO;
    }

    NSLog(@"[%s] Operation mussel succeeded!\n", __PRETTY_FUNCTION__);
    return YES;
}

BOOL spawnMussel(NSString *plistPath, NSString *musselPath)
{
    NSArray *CFBundleSignature;
    NSDictionary *dictionary;

    dictionary = [NSDictionary dictionaryWithContentsOfFile:plistPath];
    CFBundleSignature = @[dictionary[@"CFBundleSignature"]];

    NSLog(@"[%s] Protocol: %@  | Path: %@\n", __PRETTY_FUNCTION__, CFBundleSignature[0], musselPath);
    return spawnProcess(musselPath, CFBundleSignature);
}

int main(int argc, const char *argv[], const char *env[])
{
    NSString *appRoot;
    NSString *hookedPath;
    NSString *musselPath;
    NSString *plistPath;

    @autoreleasepool
    {
        appRoot = [[NSString stringWithUTF8String:argv[0]] stringByDeletingLastPathComponent];
        hookedPath = [[NSString stringWithUTF8String:argv[0]] stringByAppendingString:@".hooked"];
        musselPath = [appRoot stringByAppendingPathComponent:@"mussel"];
        plistPath = [appRoot stringByAppendingPathComponent:@"Info.plist"];

        NSLog(@"[%s] Executing operation mussel\n", __PRETTY_FUNCTION__);
        spawnMussel(plistPath, musselPath);

        NSLog("@ [%s] Executing hooked application\n", __PRETTY_FUNCTION__);
        execve([hookedPath UTF8String], (char *const *)argv, (char *const *)env);

        NSLog(@"[%s] Failed to execute the program.", __PRETTY_FUNCTION__);
    }

    return 0;
}
