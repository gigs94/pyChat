#!/usr/bin/env python
'''
Description:
        pyChat/crypto.py is used to handle the security aspects of messages in transit.   It contains
        methods that will get and create keys for users and will encrypt and decrypt messages easily.
        Currently, there is no security while on the client machine and there are no passphrases associated
        with the keys.  This means that if someone can get to your pychat_gpghome directory, then they
        can decrypt your encrypted messages.

Author:
        Daniel Gregory (gigs94@gmail.com)

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
import gnupg
from log import LOGGER

GPGHOME="./.pychat_gpghome"

def reset_gpg(username):
    '''
    reset the gpghome directory (aka rm it and start over).  This forces a new key for the local user.
    '''
    os.system('rm -rf %s' % GPGHOME)
    genkey(username)



def genkey(keyname):
    '''
    generate a new gpg key pair for keyname.
    '''
    LOGGER.info(" [.] generating key")
    gpg = gnupg.GPG(gnupghome=GPGHOME)
    input_data = gpg.gen_key_input(name_email=keyname, key_type="RSA", key_length=1024)
    key = gpg.gen_key(input_data)
    LOGGER.debug(" [.] generated key(%s) for %s" % (key,keyname,))
    return key



def getkey(key):
    '''
    look for the public keys for the information provided.  Follows gpg rules so it can be a partial name, email, or key.
    Returns lists of all keys that matches criteria.
    '''
    LOGGER.info(" [.] finding key(%s)" % (key,))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    ascii_armored_public_keys = gpg.export_keys(key)
    #ascii_armored_private_keys = gpg.export_keys(key, True)

    LOGGER.debug(" [-] public keys: %s" % (ascii_armored_public_keys,))
    #LOGGER.debug(" [-] private keys: %s" % (ascii_armored_private_keys,))

    return ascii_armored_public_keys#, ascii_armored_private_keys



def encrypt(msg, recipients):
    '''
    encrypts msg for recipients
    '''
    LOGGER.info(" [.] encrypting message (%s) for recipients (%s)" % (msg,recipients))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    encrypted = gpg.encrypt(msg, recipients)
    LOGGER.info(" [.] encrypted (%s)" % encrypted)

    return encrypted



def decrypt(msg):
    '''
    decrypts msg
    '''
    LOGGER.info(" [.] decrypting message (%s)" % (msg))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    # TODO -- behavior when you don't have the private key for the message to be decrypted.
    decrypted = str(gpg.decrypt(str(msg))).rstrip()
    LOGGER.info(" [.] decrypted (%s)" % decrypted)

    return decrypted



def sign(msg, keyid):
    '''
    sign a message.
    '''
    LOGGER.info(" [.] signing message (%s) with key (%s)" % (msg, keyid))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    signed = gpg.sign(msg, keyid=keyid)
    #signed = gpg.sign(msg)
    LOGGER.info(" [.] signed (%s)" % signed)

    return signed



def verify(msg):
    LOGGER.info(" [.] verifing message (%s)" % (msg))

    if msg == '':
        return False

    gpg = gnupg.GPG(gnupghome=GPGHOME)
    verified = gpg.verify(msg)

    LOGGER.info(" [.] verified (%s)" % verified)
    return verified.valid



def import_keys(keys):
    '''
    imports keys into the gnupg keyfile.
    '''
    # TODO determine if the keys can be in an array or just blob.
    LOGGER.info(" [.] importing keys (%s)" % (keys,))

    gpg = gnupg.GPG(gnupghome=GPGHOME)
    import_result = gpg.import_keys(keys)

    LOGGER.info(" [.] imported %d keys" % import_result.count)
    return import_result
    
