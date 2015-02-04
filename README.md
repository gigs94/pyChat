pyChat
~~~~~~

pyChat is a python based chat server that uses gpg encryption for message content security.   It's a scalable solution that utilizes a rabbitMQ server to process all interprocess communication between all clients and the server.  For ease of deployment, a basic setup script will install rabbitMQ into docker.  pyChat uses rabbitMQ, docker, and python-gnupg.


Installation
------------

Server
======

 1. Create a ubuntu (or equivalent) linux VM or machine to run the server on
 2. Download the pyChat from git hub
    git clone https://github.com/gigs94/pyChat.git
    cd pyChat
    python ./setup.py install
 3. Install docker/boot2docker
    a.  Install VirtualBox
    b.  OSX -- install boot2docker
        http://boot2docker.io/
        boot2docker_setup.sh
    c.  Linux -- install docker
        curl -sSL https://get.docker.io/ubuntu/ | sudo sh
        docker run -d -p 5672:5672 -p 15672:15672 dockerfile/rabbitmq
    d.  Windows -- Unsupported at this time
 

Client
======

 1. Download the pyChat from git hub
    git clone https://github.com/gigs94/pyChat.git
    cd pyChat
    python ./setup.py install


Running
-------

Server
======

 The server is installed in /usr/local/bin (typically) and is called pychat_server.py.   The server needs to run on the same machine as the rabbitmq server at this time.  


Client
======

  The only client at this time (the implementation just has to be able to talk to the server's protocol and to rabbitmq) is chatterbox.py.  Typically,  you would follow these steps to gain access to the system and start chatting:

 1. chatterbox.py
 2. select 6, register a new account and follow prompts
 3. select 4, login
 4. select 1, show users
 5. select 7, chat with user and follow prompts

When you are not in an active chat, you can send and receive messages in an "email" style fashion with selectors 2 & 3.  


Configuration
-------------

There is no needed configuration except for the location of the pychat and rabbitmq server which can be passed via the command line using chatterbox.py.



Known Bugs
----------
 1. There is an error on exit where a NoneType is being called.   Usually happens when nothing has been received.


Future Development
------------------

 1. Design a better GUI interface using wxpython (or equivalent)
 2. 
