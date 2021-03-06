#!/usr/bin/env python
'''
Description:
        pyChat.server.py is a chat server that manages an instance of the chat service.
        Each instance of the server runs autonomously, messages delivered to one instance
        of the server will not propogate to another instance.  It is meant to be run in
        small office environments.

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

import pyChat
import logging
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--debug',
        help='Print lots of debugging statements',
        action="store_const",dest="loglevel",const=logging.DEBUG,
        default=logging.CRITICAL
    )
    parser.add_argument('-v','--verbose',
        help='Be verbose',
        action="store_const",dest="loglevel",const=logging.INFO
    )
    args = parser.parse_args()
    pyChat.LOGGER.setLevel(level=args.loglevel)

    pyChat.run_server()
