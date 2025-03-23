#!/usr/bin/env bash

rm -rf files
cp -r src files
sed -i 's/BZHCTF{.*}/BZHCTF{placeholder}/g' files/flag.txt
cd files
zip -rm phpguru.zip *