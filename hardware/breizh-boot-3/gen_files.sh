#!/bin/bash

set -xe

# Define the output tar archive name
OUTPUT_ARCHIVE="files/breizh_boot_3.tar.gz"

# Create the tar archive with the specified files and structure
tar -czf "$OUTPUT_ARCHIVE" \
    --transform='s|^src/files/client.py|client.py|' src/files/client.py \
    --transform='s|^src/files/Dockerfile.player|Dockerfile|' src/files/Dockerfile.player \
    --transform='s|^src/files/compose.yml|compose.yml|' src/files/compose.yml \
    --transform='s|^src/files/fitImage|fitImage|' src/files/fitImage \
    --transform='s|^src/files/fake-flag.img|files/fake-flag.img|' src/files/fake-flag.img \
    --transform='s|^src/src/server.py|files/server.py|' src/src/server.py \
    --transform='s|^src/files/README.md|README.md|' src/files/README.md \
    --transform='s|^src/src/barebox-dt-2nd.img|files/barebox-dt-2nd.img|' src/src/barebox-dt-2nd.img \
    --transform='s|^src/files/convert-pem-to-breizhcertificate.py|convert-pem-to-breizhcertificate.py|' src/files/convert-pem-to-breizhcertificate.py

# Output message
echo "[BREIZH-BOOT #1] Archive '$OUTPUT_ARCHIVE' created successfully."

