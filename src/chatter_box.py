#!/usr/bin/env python


import pyChat
import time

pychat = pyChat.pychat_server('localhost')

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
    pychat.readMsgs()

def mlogin():
    pychat.login(whoami)

def main_menu():
    '''
    An easy to use menu command line interface front end for pyChat
    '''
    print "##############################################"
    print "C H A T T E R   B O X   -- a pyChat cli client"
    print ""
    print " 1. Show Users"
    print " 2. Send Message"
    print " 3. Read Message"
    print " 4. Login"
    print " 5. Logoff"
    print " 0. Quit"

    try:
        selection = raw_input('selection: ')
    except SyntaxError:
        return
    
    pyChat.log.log.debug("selection is %s" % selection)
    
    if str(selection) == '1' or str(selection) == 'show':
        show_users()
    elif str(selection) == '2' or str(selection) == 'send':
        send_msg()
    elif str(selection) == '3' or str(selection) == 'read':
        read_msg()
    elif str(selection) == '4' or str(selection) == 'login':
        mlogin()
    elif str(selection) == '5' or str(selection) == 'logoff':
        logoff()
    elif str(selection) == '0' or str(selection) == 'quit':
        quit()
    else:
        print " INVALID SELECTION... PLEASE TRY AGAIN "
        time.sleep(3)


def main():
    while (True):
        # print main menu
        selection = main_menu()


if __name__ == '__main__':
    main()
