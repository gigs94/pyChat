pyChat
~~~~~~

pyChat is a python based chat server that uses gpg encryption for message content security.   It's a scalable solution that utilizes a rabbitMQ server to process all interprocess communication between all clients and the server.

For ease of deployment, a basic setup script will install rabbitMQ into docker.   The script also run a http server where users can download the client application from.

pyChat uses rabbitMQ, docker, and python-gnupg.


Installation
------------

 1. Create a ubuntu (or equivalent) linux VM or machine
 2. Install docker/boot2docker
 3. Download the pyChat from git hub
    git clone https://github.com/gigs94/pyChat.git
 4. run the setup.py script 
    cd pyChat; python ./setup.py
 5. start the docker containers
    cd ../; python boot_docker.py
    

Unzip the file and run python setup.py




Configuration
-------------

pyChat is configured through an initial setup script
