#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <IP> <port>"
    exit 1
fi

IP=$1
PORT=$2

# Run the Python script
python3 ../files/client.py "$IP" "$PORT" list_and_read_file-out.obj