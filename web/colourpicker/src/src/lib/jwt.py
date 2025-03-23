#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mika

from sys import stdout
from jwt import decode, encode, get_unverified_header
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from base64 import urlsafe_b64decode
from lib.database import get_key_from_db, get_user_colour, get_username

def jwk_to_pem_public(jwk: dict) -> str:
    def b64_to_int(value):
        return int.from_bytes(urlsafe_b64decode(value + "=="), 'big')

    public_key = rsa.RSAPublicNumbers(
        e=b64_to_int(jwk['e']),
        n=b64_to_int(jwk['n'])
    ).public_key()

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return pem_public.decode()

def jwk_to_pem_private(jwk: dict) -> str:
    def b64_to_int(value):
        return int.from_bytes(urlsafe_b64decode(value + "=="), 'big')

    private_key = rsa.RSAPrivateNumbers(
        p=b64_to_int(jwk['p']),
        q=b64_to_int(jwk['q']),
        d=b64_to_int(jwk['d']),
        dmp1=b64_to_int(jwk['dp']),
        dmq1=b64_to_int(jwk['dq']),
        iqmp=b64_to_int(jwk['qi']),
        public_numbers=rsa.RSAPublicNumbers(
            e=b64_to_int(jwk['e']),
            n=b64_to_int(jwk['n'])
        )
    ).private_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return pem_private.decode()

def get_key(kid:str) -> dict:
    key = get_key_from_db(kid)

    if key != None:
        return {
            'id': key[0],
            'kid': key[1],
            'kty': key[2],
            'p': key[3],
            'q': key[4],
            'd': key[5],
            'e': key[6],
            'n': key[7],
            'qi': key[8],
            'dp': key[9],
            'dq': key[10]
        }
    else:
        return False

def validate_token(token: str) -> bool:
    try:
        headers = get_unverified_header(token)
        kid = headers.get('kid')
        if not kid:
            return False
        key = get_key(kid)
        if not key:
            return False

        pem_public = jwk_to_pem_public(key)

        decoded_token = decode(
            token,
            key=pem_public,
            algorithms=["RS256"]
        )

        if datetime.fromtimestamp(decoded_token['exp']) < datetime.utcnow():
            return False

        if not get_username(decoded_token['user_id']):
            return False

        return decoded_token

    except Exception as e:
        return False

def create_token(user_id: str, jwk_kid="default", colour="#cac6cc") -> str:
    key = get_key(jwk_kid)
    pem_private = jwk_to_pem_private(key)
    token = encode(payload={
        'user_id': user_id,
        'colour': colour,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=120)
    }, algorithm='RS256', headers={'kid': key['kid']}, key=pem_private)
    return token