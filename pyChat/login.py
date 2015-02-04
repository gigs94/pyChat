#!/usr/bin/env python
'''
Description:
        I don't think this is actually used...

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



from log import LOGGER
import crypto


class login():
    def __init__(uname):
        username = uname
        # check gpg to see if that username is in there
        if (exists):
            logon()
        else:
            create_new_account()

    def sign_username():
        # return signed username
        return crypto.sign(username)

    def create_new_account():
        # get server_pubkey
        # encrypt the message
        # send the message to the server
        # wait for reply
        pass

    def logon():
        # sign the username
        sun = sign_username()

        # send the signed name to the server
        # wait for reply
        pass

    def logoff():
        # sign the username
        sun = sign_username()

        # send the logoff message to the server with the signed username

    def heartbeat():
        '''
        ensures that the server knows that this client is still alive.
        '''
        # sign the username
        sun = sign_username()
        


if __name__ == '__main__':
   x = login('foo')

