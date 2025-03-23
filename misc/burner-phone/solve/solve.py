from sys import argv
import requests

if len(argv) < 2:
    print("Usage solve.py <url>")
    print("For example: python3 solve.py http://127.0.0.1:5000")
    exit(1)

url = argv[1]

phone_numbers = requests.get(f"{url}/app/company/get-phones/BurnerBZH").json()["phone_numbers"]

for phone_number in phone_numbers:
    resp = requests.get(f"{url}/app/burner/crack-password/{phone_number}").json()
    if "password" in resp:
        if resp["password"] == "Ashley":
            print(f"A phone number with password Ashley has been found: {phone_number}")
    
