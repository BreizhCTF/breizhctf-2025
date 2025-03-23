#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mika

from sqlite3 import connect
from os import path, remove
from sys import platform

db_path = path.dirname(path.abspath(__file__))+"/../db/colourpicker.db"
sql_schema_path = path.dirname(path.abspath(__file__))+"/../db/schema.sql"

if path.exists(db_path):
    remove(db_path)

conn = connect(db_path)

with open(sql_schema_path) as f:
    conn.executescript(f.read())

conn.commit()

def get_user_colour(user_id:int) -> str:
    c = conn.cursor()
    c.execute('SELECT colour FROM users WHERE id = (?)', (user_id,))
    user = c.fetchone()
    c.close()
    return user[0] if user else False

def get_key_from_db(kid:str) -> str:
    c = conn.cursor()
    c.execute('SELECT * FROM jwt_keys WHERE kid = (?)', (kid,))
    key = c.fetchone()
    c.close()
    return key

def create_user(username:str, password:str) -> None:
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    c.close()

def update_user_colour(user_id:int, colour:str) -> None:
    c = conn.cursor()
    c.execute('UPDATE users SET colour = (?) WHERE id = (?)', (colour, user_id))
    conn.commit()
    c.close()

def get_username(user_id:int) -> str:
    c = conn.cursor()
    c.execute('SELECT username FROM users WHERE id = (?)', (user_id,))
    user = c.fetchone()
    c.close()
    return user[0] if user else False

def get_user_by_name(username:str) -> dict:
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = (?)', (username,))
    user = c.fetchone()
    c.close()
    return user

def get_id_by_username(username:str) -> str:
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = '"+ username + "'")
    user = c.fetchone()
    c.close()
    return user[0] if user else False