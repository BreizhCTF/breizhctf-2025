#!/bin/bash

set -xe

challenge_name=binary_cooker
binary_name=${challenge_name}

archive_path="files/${challenge_name}.zip"

rm -f $archive_path

docker build -t "${challenge_name}" -f src/Dockerfile ./src
container=$(docker create "${challenge_name}:latest")
docker cp "${container}:/challenge/challenge" "./src/${binary_name}"
docker rm "${container}"
docker rmi "${challenge_name}"

tmpdir=$(mktemp -d)
sed 's/BZHCTF{.*}/BZHCTF{fake_flag}/g' src/flag.txt > "${tmpdir}/flag.txt"


# create the archive
rm -f "${archive_path}"
zip --junk-paths -r "${archive_path}" \
    "src/ld-2.31.so" "src/libc-2.31.so" \
    "src/${challenge_name}.c" "src/Dockerfile" \
    "src/${binary_name}" "${tmpdir}/flag.txt"

# ensure the real flag is not in the archive
set +e
zipgrep BZHCTF "${archive_path}" | grep -v 'BZHCTF{fake_flag}'
r=$?
set -e

if [ $r -eq 0 ]; then
    rm -f "${archive_path}"
    echo "ERROR: the real flag was present in the archive"
    exit 1
else
    echo "ok"
fi
