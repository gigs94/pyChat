#!/usr/bin/env python

'''
Description:
        pyChat_server.py is a chat server that manages an instance of the chat service.
        Each instance of the server runs autonomously, messages delivered to one instance
        of the server will not propogate to another instance.  It is meant to be run in
        small office environments.

Author:
        Daniel Gregory

Licence:
        The MIT License (MIT)

        Copyright (c) 2015 Daniel Gregory

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
        THE SOFTWARE.
'''

import os
import time
import gnupg
import pyChat_log


GPGHOME="./pychat_gpghome"

def genkey():
    pyChat_log.log.info(" [.] generating key")
    os.system('rm -rf %s' % GPGHOME)
    gpg = gnupg.GPG(gnupghome=GPGHOME)
    input_data = gpg.gen_key_input(name_email='pyChatServer@localhost')
    key = gpg.gen_key(input_data)
    pyChat_log.log.debug(" [.] generated key(%s)" % (key,))
    return key

def getkey(key):
    pyChat_log.log.info(" [.] finding key(%s)" % (key,))
    gpg = gnupg.GPG(gnupghome=GPGHOME)
    ascii_armored_public_keys = gpg.export_keys(key)
    ascii_armored_private_keys = gpg.export_keys(key, True)

    pyChat_log.log.debug(" [-] public keys: %s" % (ascii_armored_public_keys,))
    pyChat_log.log.debug(" [-] private keys: %s" % (ascii_armored_private_keys,))

    return ascii_armored_public_keys

if __name__ == "__main__":
    #mykey = genkey()
    key = getkey("pyChatServer@localhost")
    print "===============" + key
