#! /bin/sh

set -ex

# Zip des sources
rm -f files/authentification_ou_pas.zip
zip -r authentification_ou_pas.zip src/src/
mv authentification_ou_pas.zip files/

# Ajout du template_authentification_ou_pas.py
cat <<EOL > files/template_authentification_ou_pas.py
import requests

"""
Petit tuto pour récup les cookies malgré les redirections :
Lors du /login, attention à ne pas oublier de désactiver les redirections :)
Dans le cas contraire, tu ne recevras pas le cookie.
"""

from sys import argv
if len(argv) != 2:
    print("usage: \`python template_authentification_ou_pas.py <URL>\`")
    exit()

URL = argv[1]

# Register
url = f'{URL}/register'
data = {"username": "demo", "password": "demo"}
_ = requests.post(url, data=data)

# Login
url = f'{URL}/login'
response = requests.post(url, data=data, allow_redirects=False)
auth = response.cookies["auth"]

print(auth)

EOL

