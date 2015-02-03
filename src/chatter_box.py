#!/usr/bin/env python


import argparse
import pyChat
import time

pychat = pyChat.pychat_server('localhost')
whoami = None

def show_users():
    users = pychat.getUsers()
    pyChat.log.log.debug("users:\n%s" % users)

    print "{:^20} | {:^20} | {:^40}".format("Username", "Realname", "Email Address")
    print "{:^20} | {:^20} | {:^40}".format("========", "========", "=============")
    for i,user in enumerate(users):
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
    pyChat.log.log.debug("registering key {:20s} for username {}".format(key, whoami))
    return pychat.register(whoami, real, email, key)

def mlogin():
    whoami = raw_input('log in as? ')
    key = pyChat.getkey(whoami)
    if key == '':
        print "{} is not a registered user, please register first".format(whoami)
        return
    pyChat.log.log.debug("key {:20s} for {}".format(key, whoami))
    pychat.login(whoami)
    return whoami


def stop():
    pychat.stop()

def logoff(user):
    if user is not None:
        pychat.logoff(user)

def main_menu():
    '''
    An easy to use menu command line interface front end for pyChat
    '''
    print "####################################################"
    print "   C H A T T E R   B O X   -- a pyChat cli client"
    print ""
    print " 1. Show Users"
    print " 2. Send Message"
    print " 3. Read Message"
    print " 4. Login"
    print " 5. Logoff"
    print " 6. Register new account"
    print " 0. Quit"

    try:
        selection = raw_input('selection: ')
    except SyntaxError:
        return

    global whoami
    
    pyChat.log.log.debug("selection is %s" % selection)
    
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
    main()
