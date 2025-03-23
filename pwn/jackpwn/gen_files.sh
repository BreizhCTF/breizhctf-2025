#!/bin/bash

set -xe

challenge_name=jackpwn
binary_name=${challenge_name}

archive_path="files/${challenge_name}.zip"

docker build -t "${challenge_name}" -f src/Dockerfile ./src
container=$(docker create "${challenge_name}:latest")
docker cp "${container}:/challenge/challenge" "./src/${binary_name}"
docker rm "${container}"
docker rmi "${challenge_name}"

tmpdir=$(mktemp -d)
cp src/Dockerfile "${tmpdir}/Dockerfile"
sed -i 's/BZHCTF{.*}/BZHCTF{fake_flag}/g' "${tmpdir}/Dockerfile"
sed -i 's/gitlab-registry.ctf.bzh:5100/registry.ctf.bzh\/breizh/g' "${tmpdir}/Dockerfile"

# create the archive
rm -f "${archive_path}"
zip --junk-paths -r "${archive_path}" \
    "src/${challenge_name}.c" "${tmpdir}/Dockerfile" \
    "src/${binary_name}"
rm -rf "$tmpdir"

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
