#!/bin/sh
cp -r src/chall/* files

cd files
echo "BZHCTF{Fake_Flag}" > flag.txt

zip -rm instead.zip controller middleware models static views bot.js db.js index.js Dockerfile package.json routes.js utils.js flag.txt yarn.lock
