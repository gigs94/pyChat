#!/usr/bin/env python


import unittest
import os
import crypto

import log
import logging


##log.log.setLevel(logging.CRITICAL)


class TestCrypto(unittest.TestCase):

    def setUp(self):
        self.testkey = "asdf@asdf.asdf"
        self.testkey2 = "qwer@qwer.qwer"
        self.addCleanup(self.cleanup)

    
    def test_return_null_when_no_key_is_present(self):
        key = crypto.getkey(["some random key that should not be in the key file"]) 
        self.assertEqual(key, '')


    def test_gen_key_reset(self):
        print "test_gen_key_reset"
        '''
        reset_gpg also calls gen_key so this test will ensure both methods are working.
        '''
        crypto.reset_gpg(self.testkey)

        key = crypto.getkey(self.testkey)
        if key == '':
            key= crypto.genkey(self.testkey)
        self.assertIsNot(key, '')


    def test_message_encrypt(self):
        key = crypto.getkey(self.testkey)
        if key == '':
            key= crypto.genkey(self.testkey)
        self.assertIsNot(key, '')
        
        key2 = crypto.getkey(self.testkey2) 
        if key2 == '':
            key2 = crypto.genkey(self.testkey2)
        self.assertIsNot(key2, '')
    
        testmessage = "this is a test of the encryption message system"
    
        # this should encrypt the testmessage with key for key2
        result = crypto.encrypt(testmessage, ['qwer'])

        self.assertIsNot(testmessage, result)

        newtestmessage = crypto.decrypt(result)

        self.assertTrue(testmessage == newtestmessage)

    def test_sign(self):
        testsign = crypto.sign(self.testkey, self.testkey)
        self.assertTrue(testsign != self.testkey)
        self.assertTrue(crypto.verify(str(testsign)))


    def test_import_keys(self):
        # TODO
        pass

    def cleanup(self):
        #os.system('rm -rf %s' % crypto.GPGHOME)
        pass


if __name__ == '__main__':
    unittest.main()
