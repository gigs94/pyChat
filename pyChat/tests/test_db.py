#!/usr/bin/env python
'''
Description:
        Tests the db library functions

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
import db

import logging
import conf
import sqlite3



class TestDB(unittest.TestCase):

    def setUp(self):
        db.init_db()


    def test_reset_db(self):
        db.add_user('gigs', 'daniel', 'blah@blah.com', 'just a test for a key')
        conn = sqlite3.connect(conf.PYCHAT_DB)
        c = conn.cursor()

        c.execute('''SELECT count(*) FROM users''')

        count_pre = c.fetchall()
        conn.close()
        
        db.reset_db()

        conn = sqlite3.connect(conf.PYCHAT_DB)
        c = conn.cursor()

        c.execute('''SELECT count(*) FROM users''')

        count_post = c.fetchall()
        conn.close()

        self.assertTrue(count_pre != count_post)
        


    def test_add_user(self):
        db.add_user('gigs', 'daniel', 'blah@blah.com', 'just a test for a key')
        conn = sqlite3.connect(conf.PYCHAT_DB)
        c = conn.cursor()

        c.execute('''SELECT count(*) FROM users''')

        count = c.fetchall()
        conn.close()
        self.assertTrue(count[0][0] == 1)

    def test_get_users(self):
        db.reset_db()
        db.add_user('gigs', 'daniel', 'blah@blah.com', 'just a test for a key')
        db.add_user('gigs2', 'daniel', 'blah@blah.com', 'just a test for a key')
        db.add_user('gigs3', 'daniel', 'blah@blah.com', 'just a test for a key')

        users = db.get_users()

        self.assertTrue(len(users) == 3)


    def tearDown(self):
        os.system('rm -rf %s' % conf.PYCHAT_DB)


if __name__ == '__main__':
    conf.PYCHAT_DB = 'test_pychat.db'
    unittest.main()
