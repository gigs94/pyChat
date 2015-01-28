#!/usr/bin/env python

import os
import gnupg
import pyChat

GPGHOME="./pychat_gpghome"

def genkey():
    pyChat.log.log.info(" [.] generating key")
    os.system('rm -rf %s' % GPGHOME)
    gpg = gnupg.GPG(gnupghome=GPGHOME)
    input_data = gpg.gen_key_input(name_email='pyChatServer@localhost')
    key = gpg.gen_key(input_data)
    pyChat.log.log.debug(" [.] generated key(%s)" % (key,))
    return key

def getkey(key):
    pyChat.log.log.info(" [.] finding key(%s)" % (key,))
    gpg = gnupg.GPG(gnupghome=GPGHOME)
    ascii_armored_public_keys = gpg.export_keys(key)
    ascii_armored_private_keys = gpg.export_keys(key, True)

    pyChat.log.log.debug(" [-] public keys: %s" % (ascii_armored_public_keys,))
    pyChat.log.log.debug(" [-] private keys: %s" % (ascii_armored_private_keys,))

    return ascii_armored_public_keys
