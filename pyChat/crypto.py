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
    '''
    reset the gpghome directory (aka rm it and start over).  This forces a new key for the local user.
    '''
    os.system('rm -rf %s' % GPGHOME)
    genkey(keyname)

def genkey(keyname):
    '''
    generate a new gpg key pair for keyname.
    '''
    log.log.info(" [.] generating key")
    gpg = gnupg.GPG(gnupghome=GPGHOME)
    input_data = gpg.gen_key_input(name_email=keyname, key_type="RSA", key_length=1024)
    key = gpg.gen_key(input_data)
    log.log.debug(" [.] generated key(%s) for %s" % (key,keyname,))
    return key

def getkey(key):
    '''
    look for the public (and private) keys for the information provided.  Follows gpg rules so it can be a partial name, email, or key.
    Returns lists of all keys that matches criteria.
    '''
    log.log.info(" [.] finding key(%s)" % (key,))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    ascii_armored_public_keys = gpg.export_keys(key)
    ascii_armored_private_keys = gpg.export_keys(key, True)

    log.log.debug(" [-] public keys: %s" % (ascii_armored_public_keys,))
    log.log.debug(" [-] private keys: %s" % (ascii_armored_private_keys,))

    return ascii_armored_public_keys, ascii_armored_private_keys

def encrypt(msg, recipients):
    '''
    encrypts msg for recipients
    '''
    log.log.info(" [.] encrypting message (%s) for recipients (%s)" % (msg,recipients))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    encrypted = gpg.encrypt(msg, recipients)
    log.log.info(" [.] encrypted (%s)" % encrypted)

    return encrypted

def decrypt(msg):
    '''
    decrypts msg
    TODO -- behavior when you don't have the private key for the message to be decrypted.
    '''
    log.log.info(" [.] decrypting message (%s)" % (msg))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    decrypted = str(gpg.decrypt(str(msg)))
    log.log.info(" [.] decrypted (%s)" % decrypted)

    return decrypted


def sign(msg):
    '''
    sign a message.
    '''
    # TODO how does it know which private key to sign with??
    log.log.info(" [.] signing message (%s)" % (msg))
    gpg = gnupg.GPG(gnupghome=GPGHOME)

    signed = gpg.sign(msg)
    log.log.info(" [.] signed (%s)" % signed)

    return signed


def verify(msg):
    log.log.info(" [.] verifing message (%s)" % (msg))

    gpg = gnupg.GPG(gnupghome=GPGHOME)
    verified = gpg.verify(msg)

    log.log.info(" [.] verified (%s)" % verified)
    return verified


def import(keys):
    '''
    imports a set of keys.
    '''
    # TODO determine if the keys can be in an array or just blob.
    log.log.info(" [.] importing keys (%s)" % (keys))

    gpg = gnupg.GPG(gnupghome=GPGHOME)
    import_result = gpg.import_keys(keys)

    log.log.info(" [.] imported %d keys" % import_results.count)
    return import_results
    

if __name__ == "__main__":
    testkey = "asdf@asdf.asdf"
    testkey2 = "qwer@qwer.qwer"

    key, pKey = getkey(testkey) 
    log.log.debug(" [-] getkey returned '%s'" % key)
    if key == '':
        key= genkey(testkey)

    key2, pKey2 = getkey(testkey2) 
    log.log.debug(" [-] getkey returned '%s'" % key2)
    if key2 == '':
        key2 = genkey(testkey2)

    testmessage = "this is a test of the encryption message system"

    result = encrypt(testmessage, ['qwer'])

    newtestmessage = decrypt(result)

    if testmessage == newtestmessage:
        print "Test Successful!"
    

    testsign = sign(testkey)
    if verify(str(testsign)):
        print "verify worked"
    