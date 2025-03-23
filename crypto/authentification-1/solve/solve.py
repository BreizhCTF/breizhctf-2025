from pwn import xor
from json import dumps
import requests

# 0. Récupération de {HOST,PORT} depuis argv
from sys import argv

if len(argv) != 2:
    print("usage: `sage solve.sage <URL>`")
    exit()

URL = argv[1]


# 1. Récupération d'un ct avec clair connu
def build_pt(username, role="guest"):
    return dumps({"username": username, "role": role})


username = "skilo" + "o" * 150
pt = build_pt(username)

# on reset la db
url = f"{URL}/reset-db"
_ = requests.get(url)

# Register
url = f"{URL}/register"
headers = {"User-Agent": "solve-script"}
data = {"username": username, "password": "a"}
response = requests.post(url, headers=headers, data=data, allow_redirects=False)

# Login to get token
url = f"{URL}/login"
response = requests.post(url, headers=headers, data=data, allow_redirects=False)
token = response.cookies["auth"].replace("\\073", ";").strip('"')
ct, tag = map(bytes.fromhex, token.split(";"))

# 2. On peut maintenant récup le keystream
keystream = xor(ct, pt.encode())

# et forger le payload désiré
target_pt = build_pt("skilooooo", "super_admin")
forged_ct = xor(target_pt.encode(), keystream[: len(target_pt)])

token = forged_ct.hex() + ";" + tag.hex()

session = requests.Session()
token = '"' + token.replace(";", "\\073") + '"'
session.cookies.set("auth", token)
url = f"{URL}/admin"
response = session.get(url)

flag = "BZHCTF" + response.text.split("BZHCTF")[1].split("}")[0] + "}"
print(f"{flag = }")
