#!/usr/bin/env bash

set -xe

# pip3 install -r requirements.txt
rm -f files/cube_median.zip
cd src
rm -f encrypted_flag.png 
python3 generator.py
zip -r cube_median.zip encrypted_flag.png generator.py
mv cube_median.zip ../files
