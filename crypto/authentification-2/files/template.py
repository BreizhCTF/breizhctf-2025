import requests

"""
Petit tuto pour récup les cookies malgré les redirections :
Lors du /login, attention à ne pas oublier de désactiver les redirections :)
Dans le cas contraire, tu ne recevras pas le cookie.
"""

from sys import argv
if len(argv) != 3:
    print("usage: `python template.py <HOST> <PORT>`")
    exit()

HOST = argv[1]
PORT = int(argv[2])

# Register
url = f'http://{HOST}:{PORT}/register'
data = {"username": "demo", "password": "demo"}
_ = requests.post(url, data=data)

# Login
url = f'http://{HOST}:{PORT}/login'
response = requests.post(url, data=data, allow_redirects=False)
auth = response.cookies["auth"]

print(auth)

