# Network Security Tools

This repository contains a selection of tools I've made that have been fairly helpful (at least to me).

All of these files work through command line input, you can always add -h to find what the options are. 

The wordlists that these files use by default are included in this repository, however if you would like to download more/different wordlists there are quite a few good resources, including my wordslists repository [here](https://github.com/bagreen/Wordlists).

## Decoder

Works through an input and tries to decode it through a variety of different cryptographic methods.

Currently decodes input encoded in:
* Caesar Cipher
* Polybius Cipher
* Bacon Cipher
* Null Cipher
* Rail Cipher
* Morse Code
* Monoalphabetic Cipher
* Binary
* Octal
* Hexadecimal
* Base 16/hex
* Base 32
* Base 64/radix64
* Base 85/ascii85

## Keylogger (WIP)

Keylogger that emails the keys pressed to the specified email.

## Login_Decrypter (WIP)

Tries various passwords and usernames to login to a website. 

## MAC_Changer

Changes your MAC address on the specified interface to the specified MAC address.

## Malware_Downloader (WIP)

Downloads malware (preferably some that you have written!) on to the designated computer.

## Network_Scanner

Built to both scans your network and returns a list of the various devices that are connected, and scan ports on a device and tells you which are open. 

There's a command line option for each, so just specify which you want to do.

## PDF_Decrypter

Finds the password to a PDF using qpdf.

## Website_Scanner

Built to both spider/crawl a website and to find a website's subdirectories.

There's a command line option for each, so just specify which you want to do.

## WiFi_Decrypter (WIP)

Captures a WiFi network's handshake and attempts to decrypt the password.

# TODO

## Login_Decrypter

* Test and clean up

## Keylogger

* Need to test

## WiFi_Decrypter

* Need to figure out output from commands
