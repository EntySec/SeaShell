<h3 align="left">
    <img src="https://github.com/EntySec/SeaShell/blob/main/seashell/data/logo.png" alt="logo" height="250px">
</h3>

<p>
    <a href="https://entysec.com">
        <img src="https://img.shields.io/badge/developer-EntySec-blue.svg">
    </a>
    <a href="https://github.com/EntySec/SeaShell">
        <img src="https://img.shields.io/badge/language-Python-blue.svg">
    </a>
    <a href="https://github.com/EntySec/SeaShell/forks">
        <img src="https://img.shields.io/github/forks/EntySec/SeaShell?color=green">
    </a>
    <a href="https://github.com/EntySec/SeaShell/stargazers">
        <img src="https://img.shields.io/github/stars/EntySec/SeaShell?color=yellow">
    </a>
    <a href="https://www.codefactor.io/repository/github/EntySec/SeaShell">
        <img src="https://www.codefactor.io/repository/github/EntySec/SeaShell/badge">
    </a>
</p>

SeaShell Framework is an iOS post-exploitation framework that exploits the CoreTrust bug to remotely access an iPhone or iPad.

## Features

* **IPA generator** - All you need to do is generate an IPA file and install it on a target's device via [TrollStore](https://trollstore.app/) or other IPA installer that bypasses CoreTrust. After app was installed, a target simply need to run an app single time.
* **Powerful Implant** - SeaShell Framework uses the advanced and powerful payload with lots of features. It is called [Pwny](https://github.com/EntySec/Pwny). You can extend it by adding your own post-exploitation modules or plugins.
* **Basic Set** - SeaShell Framework comes with basic set of post-exploitation modules that may exfiltrate following user data: DCIM, SMS, VoiceMail, Safari history and much more.

## Usage

### Generating IPA

Simply generate custom IPA file and install it on target's iPhone or iPad.

![1]()

### Staring listener

Then you will need to start a listener on a host and port you added to your IPA. Once installed application opens, you will receive a session.

![2]()

### Accessing device

After you received a connection you will be able to communicate with session through a shell. Use `interact` to interact and `help` to view list of all available commands. You can even extract Safari history like in the example below.

![3]()

## Covering them All

Wide range of iOS versions are supported, since all of the are vulnerable to CoreTrust bug. They can be iOS 14, 15, 16 or early 17. Since

## Endless Capabilities

[Pwny](https://github.com/EntySec/Pwny) is a powerful implant with a plenty of features including evasion, dynamic extensions and much more. It is embedded into the second phase of SeaShell Framework attack. These are all phases:

* **1.** IPA file installed and opened.
* **2.** Pwny is loaded through `posix_spawn()`.
* **3.** Connection established and Pwny is ready to receive commands.
