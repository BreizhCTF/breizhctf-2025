#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mika

from flask import Flask, request, jsonify, redirect, make_response, render_template
from secrets import token_hex
from bcrypt import hashpw, gensalt
from functools import wraps
from time import sleep 
from re import match
from jinja2 import Template
from os import environ

from lib.database import create_user, update_user_colour, get_user_colour, get_username, get_user_by_name, get_id_by_username
from lib.jwt import validate_token, create_token, get_key

app = Flask(__name__)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not 'token' in request.cookies:
            return redirect('/login')
        if not validate_token(request.cookies.get('token')):
            response = make_response(render_template('login.html', error='Token invalide ou expiré, merci de réessayer'))
            response.set_cookie('token', '', expires=0)
            return response
        return f(*args, **kwargs)
    return wrapper

def not_logged_in(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'token' in request.cookies:
            if validate_token(request.cookies.get('token')) != False:
                return redirect('/')
        return f(*args, **kwargs)
    return wrapper

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    token = validate_token(request.cookies.get('token'))
    user_id = token['user_id']
    username = get_username(user_id)
    user_colour = token['colour']
    if request.method == 'GET':
        #SSTI Here
        user_colour_template = "%s" % user_colour
        user_colour = Template(user_colour_template).render()
        return render_template('index.html', user_colour=user_colour, username=username, user_id=get_id_by_username(username))
    if request.method == 'POST':
        if 'colour' in request.form: 
            new_colour = request.form.get('colour')
            if not match(r'^#(?:[0-9a-fA-F]{4}){1,2}$', new_colour):
                return render_template('index.html', error='La couleur ne répond pas à cette RegEx : ^#(?:[0-9a-fA-F]{4}){1,2}$', username=username, user_colour=user_colour, user_id=get_id_by_username(username))
            token = create_token(user_id=user_id, colour=new_colour)
            response = make_response(redirect('/'))
            response.set_cookie('token', token)
            return response
        else:
            return render_template('index.html', error='Pas de couleur envoyée', username=username, user_colour=user_colour, user_id=get_id_by_username(username))

@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if 'register' in request.form:
            user = get_user_by_name(request.form.get('username'))
            if user:
                return render_template('login.html', error='Cet utilisateur existe déjà')
            
            # Blacklist characters
            BLACKLIST = [" ", "\"", "<", ">", "script", "=", ";", "-", "--", "/**/"]
            for blacklisted in BLACKLIST:
                if blacklisted in request.form.get('username'):
                    return render_template('login.html', error=f'Les caractères suivants ne sont pas permis: {BLACKLIST}')
            s_quote_count = 0
            for char in request.form.get('username'):
                if char == "'":
                    s_quote_count += 1
            if s_quote_count > 1:
                return render_template('login.html', error='Oups, vous ne pouvez pas avoir plus d\'une simple quote dans votre nom d\'utilisateur.')
            #######################

            create_user(request.form.get('username'), hashpw(request.form.get('password').encode(), gensalt()).decode())
            return render_template('login.html', success='Utilisateur créé, vous pouvez maintenant vous connecter')
        else:
            user = get_user_by_name(request.form.get('username'))
            if not user:
                return render_template('login.html', error='Utilisateur non trouvé.')
            if not hashpw(request.form.get('password').encode(), user[2].encode()) == user[2].encode():
                return render_template('login.html', error='Mot de passe incorrect.')
            token = create_token(user[0])
            response = make_response(redirect('/'))
            response.set_cookie('token', token)
            return response

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('token', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=environ.get('DEBUG', False), threaded=False, use_reloader=False, host='0.0.0.0')