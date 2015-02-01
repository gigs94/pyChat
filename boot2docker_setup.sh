#!/usr/bin/env bash

boot2docker upgrade
boot2docker stop; boot2docker -v delete ; boot2docker -v upgrade ; boot2docker -v init ; boot2docker -v up
$(/usr/local/bin/boot2docker shellinit)

docker run -d -p 5672:5672 -p 15672:15672 dockerfile/rabbitmq 

curl localhost:5672 >> test_rabbitmq
curl localhost:15672 >> test_rabbitmq2

VBoxManage controlvm boot2docker-vm natpf1 "__5672,tcp,127.0.0.1,5672,,5672"
VBoxManage controlvm boot2docker-vm natpf1 "__15672,tcp,127.0.0.1,15672,,15672"

