# pyChat

pyChat is a python based chat server that uses gpg encryption for message content security.   It's a scalable solution that utilizes a rabbitMQ server to process all interprocess communication between all clients and the server.

For ease of deployment, a basic setup script will install rabbitMQ, couchDB into docker.   The script also run a http server where users can download the client application from.

pyChat uses rabbitMQ, docker, couchdb, python-gnupg, pyinstaller, and unittest.


## Installation

 0. Create a ubuntu (or equivalent) linux VM or machine
 1. Install docker and boot2docker
 2. Download the pyChat from git hub
    git clone https://github.com/gigs94/pyChat.git
 3. run the setup.py script 
    cd pyChat; python ./setup.py
 4. start the docker containers
    

Unzip the file and run python setup.py

## Configuration

pyChat is configured through an initial setup script
