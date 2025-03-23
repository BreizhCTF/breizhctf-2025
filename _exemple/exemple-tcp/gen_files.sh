#!/usr/bin/env bash

set -xe

docker build -t chall .

docker run -d --name instance chall

docker cp instance:/challenge/challenge ./files/challenge

docker kill instance
docker rm instance
docker rmi chall
