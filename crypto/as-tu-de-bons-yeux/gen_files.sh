#! /bin/sh

set -ex

rm -f files/as-tu-de-bons-yeux.zip
zip -r as-tu-de-bons-yeux.zip src/src/
mv as-tu-de-bons-yeux.zip files/
