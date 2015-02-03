#!/usr/bin/env python


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

