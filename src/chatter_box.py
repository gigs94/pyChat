#!/usr/bin/env python
'''
Description:
        Chatter Box is a command line implementation of the pychat protocol.  Very
        basic and lots of improvements can be made.

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


import argparse
import pyChat
import time
msleep = lambda x: time.sleep(x/1000.0)

import logging
import threading

pychat = None
whoami = None

def show_users():
    users = pychat.getUsers()
    pyChat.LOGGER.debug("users:\n%s" % users)

    print "{:^20} | {:^20} | {:^40}".format("Username", "Realname", "Email Address")
    print "{:^20} | {:^20} | {:^40}".format("========", "========", "=============")
    for user in users:
        print "{:<20} | {:<20} | {:<40}".format(user[0], user[1], user[2])

def send_msg():
    show_users()

    try:
        who = raw_input("Which user to send to? ")
        what = raw_input("Please type the message to send: ")
    except SyntaxError:
        return

    pychat.sendmsg(who, what)

def read_msg():
    print pychat.readmsg()

def register():
    global whoami
    whoami = raw_input('register userid: ')
    real = raw_input('real name: ')
    email = raw_input('email: ')
    key = pyChat.getkey(whoami)
    if key == '':
        key = pyChat.genkey(whoami)
    pyChat.LOGGER.debug("registering key {:20s} for username {}".format(key, whoami))
    return pychat.register(whoami, real, email, key)

def mlogin():
    whoami = raw_input('log in as? ')
    key = pyChat.getkey(whoami)
    if key == '':
        print "{} is not a registered user, please register first".format(whoami)
        return
    pyChat.LOGGER.debug("key {:20s} for {}".format(key, whoami))
    pychat.login(whoami)
    return whoami


def stop():
    pychat.stop()

def logoff(user):
    if user is not None:
        pychat.logoff(user)
        global whoami
        whoami = None


def interactive_read(_stop, user):
    '''
    Chat with a user
    '''
    while(not _stop.isSet()):
        for body in pychat.readmsg(user):
            print "{:>60}".format(body)
        msleep(1)
        

def interactive():
    '''
    continously prints inbound messages and outbound messages to the screen
    for more 'interactive' session
    '''
    show_users()
    user = raw_input("Who would you like to chat with? ")
    print "type ^C to exit"
    print ""

    _stop = threading.Event()
    t = threading.Thread(target=interactive_read, args=(_stop, user, ))
    t.daemon = True
    t.start()

    while(True):
        try:
            send = raw_input('')
        except SyntaxError:
            break
        except KeyboardInterrupt:
            break
        pychat.sendmsg(user, send)

    _stop.set()

def main_menu():
    '''
    An easy to use menu command line interface front end for pyChat
    '''

    global whoami

    print "####################################################"
    print "   C H A T T E R   B O X   -- a pyChat cli client"
    print ""
    if whoami is not None:
        print "    logged in as: {0}".format(whoami)
        print ""
    
    print " 1. Show Users"
    print " 2. Send Message"
    print " 3. Read Message"
    print " 4. Login"
    print " 5. Logoff"
    print " 6. Register new account"
    print " 7. Chat with user"
    print " 0. Quit"

    try:
        selection = raw_input('selection: ')
    except SyntaxError:
        return

    
    pyChat.LOGGER.debug("selection is %s" % selection)
    
    if str(selection) == '1' or str(selection) == 'show':
        show_users()
    elif str(selection) == '2' or str(selection) == 'send':
        send_msg()
    elif str(selection) == '3' or str(selection) == 'read':
        read_msg()
    elif str(selection) == '4' or str(selection) == 'login':
        whoami=mlogin()
    elif str(selection) == '5' or str(selection) == 'logoff':
        logoff(whoami)
    elif str(selection) == '6' or str(selection) == 'register':
        register()
    elif str(selection) == '7' or str(selection) == 'chat':
        interactive()
    elif str(selection) == '0' or str(selection) == 'quit' or str(selection) == 'q':
        stop()
        quit()
    else:
        print " INVALID SELECTION... PLEASE TRY AGAIN "
        time.sleep(1)

def main():
    while (True):
        # print main menu
        selection = main_menu()

if __name__ == '__main__':

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
    parser.add_argument('-s','--server',
        help='name or ip of the server to connect to',
        dest="server",default='localhost'
    )
    args = parser.parse_args()    
    pyChat.LOGGER.setLevel(level=args.loglevel)

    pyChat.conf.HOST = args.server
    pychat = pyChat.pychat_server(args.server)

    main()
