#!/usr/bin/env python
'''
Description:
        Tests the crypto library functions

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


import unittest
import os
import crypto

import logging



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
