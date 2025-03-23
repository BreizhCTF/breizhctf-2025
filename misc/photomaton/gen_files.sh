#! /bin/bash

set -ex

rm -rf files/Photomaton.zip
cd src
rm -f goodluck.png
python3 photomaton.py
zip -r Photomaton.zip photomaton.py goodluck.png
mv Photomaton.zip ../files/

