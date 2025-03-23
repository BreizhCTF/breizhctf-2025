#!/usr/bin/env bash

rm -rf files
cp -r src files
sed -i 's/BZHCTF{.*}/BZHCTF{placeholder}/g' files/compose.yml
sed -i 's/VAULT_PIN=.*$/VAULT_PIN=123456/g' files/compose.yml
sed -i 's/gitlab-registry.ctf.bzh:5100/registry.ctf.bzh\/breizh/g' files/app/Dockerfile
cd files
zip -rm vaultmania.zip *