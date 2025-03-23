#! /bin/sh

set -ex

# Zip des sources
rm -f files/authentification_le_retour.zip
zip -r authentification_le_retour.zip src/src/
mv authentification_le_retour.zip files/

# Ajout du template.py
cat <<EOL > files/template_authentification_le_retour.py
import requests

"""
Petit tuto pour récup les cookies malgré les redirections :
Lors du /login, attention à ne pas oublier de désactiver les redirections :)
Dans le cas contraire, tu ne recevras pas le cookie.
"""

from sys import argv
if len(argv) != 2:
    print("usage: \`python template_authentification_le_retour.py <URL>\`")
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

