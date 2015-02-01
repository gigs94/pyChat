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



Configuration
-------------

There is no needed configuration except for the location of the rabbitmq server which can be passed via the command line using chatterbox.py.



