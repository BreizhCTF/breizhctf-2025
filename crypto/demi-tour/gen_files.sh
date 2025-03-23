#! /bin/sh

set -ex

# zip les sources
rm -f files/demi-tour.zip
zip -r demi-tour.zip src/
mv demi-tour.zip files/demi-tour.zip

