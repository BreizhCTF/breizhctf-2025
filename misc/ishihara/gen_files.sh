#!/usr/bin/env bash

if [ "$#" -eq 0 ]; then
  echo "Usage: ./gen_files.sh 'BZHCTF{1shih4rA_?never_he4rd_ab0ut!}'"
else
    rm -rf ./files ./src/challenge ./src/ishihara ./src/letters
    mkdir ./files ./src/challenge ./src/ishihara ./src/letters
    cd src
    python3 generate.py letters
    python3 generate.py flag --flag $1
    zip Ishihara.zip challenge/*.png
    mv Ishihara.zip ../files/
    #rm -rf ./challenge ./ishihara ./letters
fi