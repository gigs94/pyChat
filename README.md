# pyChat

pyChat is a python based chat server that uses gpg encryption for message handling and simple server interface with rabbitMQ.

It is a project that uses docker containers run each service in the presumption that this will enable better behavior and performance in the long term as these services will evolve and be maintained better than any home rolled solution will.

pyChat uses rabbitMQ, docker, couchdb, python-gnupg, pyinstaller, sphinx, and unittest.

## Installation

Simply download the .zip file onto a linux distribution that has the following packages, !!!TODO!!!

Unzip the file and run python setup.py

## Configuration

pyChat is configured through an initial setup script
