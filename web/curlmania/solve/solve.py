import sys
import re
import requests
from requests.adapters import HTTPAdapter


class CustomHTTPAdapter(HTTPAdapter):
    def send(self, request, **kwargs):
        request.headers["Content-Length"] = 1337
        request.body = request.body.rjust(1337)
        return super().send(request, **kwargs)


def main(url: str):
    session = requests.Session()
    session.mount("http://", CustomHTTPAdapter())
    session.mount("https://", CustomHTTPAdapter())

    r = session.get(
        f"{url}/1337",
        params={"a": "a", "b": "b", "35": "35"},
        headers={
            "User-Agent": "J'aime la galette saucisse",
            "LIBEREZ-GCC": "OUI",
            "Referer": "Je jure solennellement que mes intentions sont mauvaises mais je ne vais pas taper sur l'infra",
        },
        cookies={"jaiplustropdinspi": "1"},
        json={"enbretagne": "il fait toujours beau"},
        timeout=30,
    )

    assert "BZHCTF" in r.text

    success = re.search("<h3>(.*BZHCTF.*)</h3>", r.text, re.IGNORECASE)
    if success:
        print(success.group(1))


if __name__ == "__main__":
    # Check if an argument is provided
    if len(sys.argv) < 2:
        print("Error: No URL provided.")
        print("Usage: python solve.py <url>")
        sys.exit(1)

    # Get the URL from the argument
    url = sys.argv[1]
    main(url)
