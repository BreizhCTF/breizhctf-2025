#!/bin/bash

set -xe

sudo docker build -t bank_simulator -f src/Dockerfile.build src
sudo docker run -d --name bank_simulator bank_simulator:latest
sudo docker cp bank_simulator:/app/bank-simulator ./files/

# Clean tout
sudo docker rm bank_simulator
sudo docker rmi bank_simulator

