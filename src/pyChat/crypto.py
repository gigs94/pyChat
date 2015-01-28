#!/usr/bin/env python
'''
pyChat/crypto.py is used to handle the security aspects of messages in transit.   It contains
methods that will get and create keys for users and will encrypt and decrypt messages easily.
Currently, there is no security while on the client machine and there are no passphrases associated
with the keys.  This means that if someone can get to your pychat_gpghome directory, then they
can decrypt your encrypted messages.
'''

import os
import gnupg
import log

GPGHOME="./.pychat_gpghome"

def reset_gpg(keyname):
    os.system('rm -rf %s' % GPGHOME)
    genkey(keyname)

def genkey(keyname):
    log.log.info(" [.] generating key")
    gpg = gnupg.GPG(gnupghome=GPGHOME)
    input_data = gpg.gen_key_input(name_email=keyname, key_type="RSA", key_length=1024)
    key = gpg.gen_key(input_data)
    log.log.debug(" [.] generated key(%s) for %s" % (key,keyname,))
    return key

def getkey(key):
    log.log.info(" [.] finding key(%s)" % (key,))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    ascii_armored_public_keys = gpg.export_keys(key)
    ascii_armored_private_keys = gpg.export_keys(key, True)

    log.log.debug(" [-] public keys: %s" % (ascii_armored_public_keys,))
    log.log.debug(" [-] private keys: %s" % (ascii_armored_private_keys,))

    return ascii_armored_public_keys, ascii_armored_private_keys

def encrypt(msg, recipients):
    log.log.info(" [.] encrypting message (%s) for recipients (%s)" % (msg,recipients))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    encrypted = gpg.encrypt(msg, recipients)
    log.log.info(" [.] encrypted (%s)" % encrypted)

    return encrypted

def decrypt(msg):
    log.log.info(" [.] decrypting message (%s)" % (msg))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    decrypted = str(gpg.decrypt(str(msg)))
    log.log.info(" [.] decrypted (%s)" % decrypted)

    return decrypted
    

if __name__ == "__main__":
    testkey = "asdf@asdf.asdf"
    key, pKey = getkey(testkey) 
    log.log.debug(" [-] getkey returned '%s'" % key)
    if key == '':
        key= genkey(testkey)

    key2= genkey("qwer@qwer.qwer")
    #gpg.import_keys(key2)

    testmessage = "this is a test of the encryption message system"

    result = encrypt(testmessage, ['qwer'])

    newtestmessage = decrypt(result)

    if testmessage == newtestmessage:
        print "Test Successful!"
    
