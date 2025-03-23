from requests import Session
from bs4 import BeautifulSoup

URL = "http://localhost:8001"

while True:
    print("Enter the payload to send to the server:")
    payload = input("> ")
    s = Session()
    s.post(URL + "/login", data={"username": payload, "password": "password", "register": "on"})
    s.post(URL + "/login", data={"username": payload, "password": "password"})
    r = s.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.find("p", {"id": "id"}).text.replace("User ID: ", ""))
    s.close()