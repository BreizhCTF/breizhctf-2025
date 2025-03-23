from sys import argv
import requests

if len(argv) < 2:
    print("Usage solve.py <url>")
    exit(1)

url = argv[1]

response = requests.get(f"{url}/secret")
assert response.status_code == 200, 'Invalid response'
assert 'BZHCTF{}' in response.text, 'Flag not in response'

print(response.text)
