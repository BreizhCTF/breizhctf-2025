#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mika

from flask import Flask, render_template, request
from requests import post
from re import match
from os import environ

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/designer', methods=['GET'])
def designer():
    autoclick = False
    button_attributes = {
        "autofocus": 0,
        "disabled": 0,
        "commandfor": 0,
        "command": 0,
        "type": 0,
        "name": 0,
        "form": 0,
        "style": 0,
    }
    link_attributes = {
        "href": "http://localhost.local/",
        "rel": 0,
        "target": 0,
        "hreflang": 0,
    }

    if len(request.args) > 0:
        try:
            if 'autoclick' in request.args:
                autoclick = True

            for key, value in request.args.items():
                if key == 'autoclick':
                    continue
                elif key.startswith('CUSTOMATTR-'):
                    button_attributes[key.split('-')[1]] = value
                elif key in button_attributes:
                    if value=='none' and key in button_attributes:
                        button_attributes.pop(key)
                    else:
                        button_attributes[key] = value
                else:
                    if value=='none' and key in link_attributes:
                        link_attributes.pop(key)
                    else:
                        link_attributes[key] = value
        except Exception as e:
            return render_template('designer.html', error=e)
        
        print(button_attributes)
        print(link_attributes)

        html_button = f'<button'
        for key, value in button_attributes.items():
            if value != 0 and value != 'none' and value != '':
                print(key,value)
                if match(r'^[a-z]+$', key):
                    if value == 'on':
                        html_button += f' {key}'
                    else:
                        html_button += ' %s="%s"' % (key, value.replace('"', ''))
                else:
                    return render_template('designer.html', error='Les noms d\'attributs doivent être en minuscules.')
        html_button += f'>VOTRE BOUTON</button></a>'
        
        html_link = f'<a'
        for key, value in link_attributes.items():
            if value != 0 and value != 'none' and value != '':
                if match(r'^[a-z]+$', key):
                    if value == 'on':
                        html_link += f' {key}'
                    else:
                        html_link += ' %s="%s"' % (key, value.replace('"', ''))
                else:
                    return render_template('designer.html', error='Les noms d\'attributs doivent être en minuscules.')
        html_link += f'>'
    
        final = f'{html_link}{html_button}'

        return render_template('designer.html', generated=True, button=final, autoclick=autoclick)
    else:
        return render_template('designer.html')

@app.route('/report', methods=['POST', 'GET'])
def report():
    if request.method == 'POST':
        if 'url' in request.form:
            url = request.form['url']
            if url == '':
                return render_template('report.html', error='Merci de renseigner une URL à signaler.')
            if not url.startswith('/'):
                return render_template('report.html', error=f'Votre signalement doit contenir uniquement le path de l\'URL. Exemple : /designer?autoclick=on')
            else:
                try:
                    post(environ.get('ADMIN_ENDPOINT', 'http://bot:8000/report'), json={'url': url})
                except Exception as e:
                    return render_template('report.html', error=f"Impossible de signaler aux administrateurs. {e}")
                return render_template('report.html', success="Signalement effectué, merci d'attendre que les administrateurs consultent votre signalement.")
        else:
            return render_template('report.html', error='Merci de renseigner une URL à signaler.')
    else:
        return render_template('report.html')
if __name__ == '__main__':
    app.run(debug=environ.get('DEBUG', False), host='0.0.0.0')