<h3 align="left">
    <img src="https://github.com/EntySec/SeaShell/blob/main/seashell/data/logo.png" alt="logo" height="250px">
</h3>

[![Developer](https://img.shields.io/badge/developer-EntySec-blue.svg)](https://entysec.com)
[![Language](https://img.shields.io/badge/language-Python-blue.svg)](https://github.com/EntySec/SeaShell)
[![Forks](https://img.shields.io/github/forks/EntySec/SeaShell?style=flat&color=green)](https://github.com/EntySec/SeaShell/forks)
[![Stars](https://img.shields.io/github/stars/EntySec/SeaShell?style=flat&color=yellow)](https://github.com/EntySec/SeaShell/stargazers)
[![CodeFactor](https://www.codefactor.io/repository/github/EntySec/SeaShell/badge)](https://www.codefactor.io/repository/github/EntySec/SeaShell)

[SeaShell Framework](https://blog.entysec.com/2023-12-31-seashell-ios-malware/) is an iOS post-exploitation framework that enables you to access the device remotely, control it and extract sensitive information.

## Features

* **IPA generator** - All you need to do is generate an IPA file and install it on a target's device via [TrollStore](https://trollstore.app/) or other IPA installer that bypasses CoreTrust. After app was installed, a target simply need to run an app single time (he may close application completely after this).
* **Powerful Implant** - SeaShell Framework uses the advanced and powerful payload with lots of features. It is called [Pwny](https://github.com/EntySec/Pwny). You can extend it by adding your own post-exploitation modules or plugins.
* **Basic Set** - SeaShell Framework comes with basic set of post-exploitation modules that may exfiltrate following user data: SMS, VoiceMail, Safari history and much more.
* **Encrypted communication** - Communication between device and SeaShell is encrypted using the [TLS 1.3](https://en.wikipedia.org/wiki/Transport_Layer_Security) encryption by default.
* **Regular updates** - SeaShell Framework is being actively updated, so don't hesitate and leave your [feature request](https://github.com/EntySec/SeaShell/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=)!

## Installation

To install SeaShell Framework you just need to type this command in your terminal:

```shell
pip3 install git+https://github.com/EntySec/SeaShell
```

After this SeaShell can be started with `seashell` command.

## Updating

To update SeaShell and get new commands run this:

```shell
pip3 install --force-reinstall git+https://github.com/EntySec/SeaShell
```

## Usage

### Generating IPA

Simply generate custom IPA file or patch existing one and install it on target's iPhone or iPad via [TrollStore](https://trollstore.app/) or other IPA installer that bypasses CoreTrust.

<p align="center">
  <img width="70%" src="https://raw.githubusercontent.com/EntySec/SeaShell/main/seashell/data/preview/ipa.svg">
</p>

### Starting listener

Then you will need to start a listener on a host and port you added to your IPA. Once the installed application opens, you will receive a connection.

<p align="center">
  <img width="70%" src="https://raw.githubusercontent.com/EntySec/SeaShell/main/seashell/data/preview/listen.svg">
</p>

### Accessing device

Once you have received the connection, you will be able to communicate with the session through a [Pwny](https://github.com/EntySec/Pwny) interactive shell. Use `devices -i <id>` to interact and `help` to view list of all available commands. You can even extract Safari history like in the example below.

<p align="center">
  <img width="70%" src="https://raw.githubusercontent.com/EntySec/SeaShell/main/seashell/data/preview/safari.svg">
</p>

## Covering them All

A wide range of iOS versions are supported, being 14.0 beta 2 - 16.6.1, 16.7 RC, and 17.0 beta 1 - 17.0, as these versions are vulnerable to the CoreTrust bug.

## Endless Capabilities

[Pwny](https://github.com/EntySec/Pwny) is a powerful implant with plenty of features including evasion, dynamic extensions and much more. It is embedded into the second phase of SeaShell Framework attack. These are all phases:

* **1.** IPA file installed and opened.
* **2.** Pwny is loaded through `posix_spawn()`.
* **3.** Connection established and Pwny is ready to receive commands.

## Issues and Bugs

SeaShell was just released and is in **BETA** stage for now. If you find a bug or some function that does not work we will be glad if you immediately submit an issue describing a problem. The more details the issue contains the faster we will be able to fix it.

## External Resources

* Medium: [SeaShell: iOS 16/17 Remote Access](https://medium.com/@enty8080/seashell-ios-16-17-remote-access-41cc3366019d)
* iDeviceCentral: [iOS Malware Makes TrollStore Users Vulnerable To Monitoring, File Extraction & Remote Control on iOS 14 – iOS 17](https://idevicecentral.com/news/ios-malware-makes-trollstore-users-vulnerable-to-monitoring-file-extraction-remote-control-on-ios-14-ios-17/)
* TheAppleWiki: [SeaShell](https://theapplewiki.com/wiki/SeaShell)

## Legal Use

Note that the code and methods provided in this repository must not be used for malicious purposes and should only be used for testing and experimenting with devices **you own**. Please consider out [Terms of Service](https://github.com/EntySec/SeaShell/blob/main/TERMS_OF_SERVICE.md) before using the tool.
