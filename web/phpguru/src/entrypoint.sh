#!/bin/bash

SECRET=$(cat /dev/urandom | tr -dc 'a-f0-9' | head -c 32)
mv /flag.txt "/flag_$SECRET.txt"

python3 -m http.server --bind 127.0.0.1 --directory '/' 8000 &

PASSWORD=$(cat /dev/urandom | tr -dc 'a-f0-9' | head -c 32) apache2-foreground