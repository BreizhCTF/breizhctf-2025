#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Mika

from flask import Flask, request, render_template, redirect
from os import environ
from copy import deepcopy

app = Flask(__name__)

rules = [
        "1. Acceder a la page /1337 ❌",
        "2. Votre user-agent doit etre \"J'aime la galette saucisse\" ❌",
        "3. Votre requete doit utiliser la methode GET et compter 3 parametres GET dont un ayant pour valeur \"35\" ❌",
        "4. Un header HTTP \"LIBEREZ-GCC: OUI\" doit etre present ❌", 
        "5. Un cookie \"jaiplustropdinspi\" est obligatoire ❌",
        "6. Le content-type doit etre \"application/json\" ❌",
        "7. Nul autre payload de data que \"enbretagne\" (JSON) ne doit etre present ❌",
        "8. La valeur du parametre de la regle 7 ne peut etre que \"il fait toujours beau\" ❌",
        "9. Le content-length doit etre de 1337 ❌",
        "10. Votre referer doit etre \"Je jure solennellement que mes intentions sont mauvaises mais je ne vais pas taper sur l'infra\" ❌",
]

@app.route('/', methods=['GET'])
def index():
    global rules
    correct = 0
    rules_tmp = deepcopy(rules)
    if request.headers.get('User-Agent') == "J'aime la galette saucisse":
        rules_tmp[1] = "2. Votre user-agent doit etre \"J'aime la galette saucisse\" ✅"
        correct += 1
    if len(request.args) == 3 and "35" in request.args.values():
        rules_tmp[2] = "3. Votre requete doit utiliser la methode GET et compter 3 parametres GET dont un ayant pour valeur \"35\"  ✅"
        correct += 1
    if request.headers.get('LIBEREZ-GCC') == "OUI":
        rules_tmp[3] = "4. Un header HTTP \"LIBEREZ-GCC: OUI\" doit etre present ✅"
        correct += 1
    if request.cookies.get('jaiplustropdinspi'):
        rules_tmp[4] = "5. Un cookie \"jaiplustropdinspi\" est obligatoire ✅"
        correct += 1
    if request.headers.get('Content-Type') == "application/json":
        rules_tmp[5] = "6. Le content-type doit etre \"application/json\" ✅"
        correct += 1
    if request.headers.get('Content-type') == "application/json" and request.json.get('enbretagne') and len(request.json) == 1:
        rules_tmp[6] = "7. Nul autre payload de data que \"enbretagne\" (JSON) ne doit etre present ✅"
        correct += 1
    if request.headers.get('Content-type') == "application/json" and request.json.get('enbretagne') == "il fait toujours beau" and len(request.json) == 1:
        rules_tmp[7] = "8. La valeur du parametre de la regle 7 ne peut etre que \"il fait toujours beau\" ✅"
        correct += 1
    if request.headers.get('Content-Length') == "1337":
        rules_tmp[8] = "9. Le content-length doit etre de 1337 ✅"
        correct += 1
    if request.headers.get('Referer') == "Je jure solennellement que mes intentions sont mauvaises mais je ne vais pas taper sur l'infra":
        rules_tmp[9] = "10. Votre referer doit etre \"Je jure solennellement que mes intentions sont mauvaises mais je ne vais pas taper sur l'infra\" ✅"
        correct += 1
    if correct == 10:
        return render_template('index.html', rules=rules_tmp, user_agent=request.headers.get('User-Agent'), flag=environ.get('FLAG', "BZHCTF{PLACEHOLDER}"))
    else:
        return render_template('index.html', rules=rules_tmp, user_agent=request.headers.get('User-Agent'))

@app.route('/1337', methods=['GET'])
def one_three_three_seven():
    global rules
    correct = 1
    rules_tmp = deepcopy(rules)
    rules_tmp[0] = "1. Acceder a la page /1337 ✅"
    if request.headers.get('User-Agent') == "J'aime la galette saucisse":
        rules_tmp[1] = "2. Votre user-agent doit etre \"J'aime la galette saucisse\" ✅"
        correct += 1
    if len(request.args) == 3 and "35" in request.args.values():
        rules_tmp[2] = "3. Votre requete doit utiliser la methode GET et compter 3 parametres GET dont un ayant pour valeur \"35\"  ✅"
        correct += 1
    if request.headers.get('LIBEREZ-GCC') == "OUI":
        rules_tmp[3] = "4. Un header HTTP \"LIBEREZ-GCC: OUI\" doit etre present ✅"
        correct += 1
    if request.cookies.get('jaiplustropdinspi'):
        rules_tmp[4] = "5. Un cookie \"jaiplustropdinspi\" est obligatoire ✅"
        correct += 1
    if request.headers.get('Content-Type') == "application/json":
        rules_tmp[5] = "6. Le content-type doit etre \"application/json\" ✅"
        correct += 1
    if request.headers.get('Content-type') == "application/json" and request.json.get('enbretagne') and len(request.json) == 1:
        rules_tmp[6] = "7. Nul autre payload de data que \"enbretagne\" (JSON) ne doit etre present ✅"
        correct += 1
    if request.headers.get('Content-type') == "application/json" and request.json.get('enbretagne') == "il fait toujours beau" and len(request.json) == 1:
        rules_tmp[7] = "8. La valeur du parametre de la regle 7 ne peut etre que \"il fait toujours beau\" ✅"
        correct += 1
    if request.headers.get('Content-Length') == "1337":
        rules_tmp[8] = "9. Le content-length doit etre de 1337 ✅"
        correct += 1
    if request.headers.get('Referer') == "Je jure solennellement que mes intentions sont mauvaises mais je ne vais pas taper sur l'infra":
        rules_tmp[9] = "10. Votre referer doit etre \"Je jure solennellement que mes intentions sont mauvaises mais je ne vais pas taper sur l'infra\" ✅"
        correct += 1
    if correct == 10:
        return render_template('index.html', rules=rules_tmp, user_agent=request.headers.get('User-Agent'), flag=environ.get('FLAG', "BZHCTF{PLACEHOLDER}"))
    else:
        return render_template('index.html', rules=rules_tmp, user_agent=request.headers.get('User-Agent'))
if __name__ == '__main__':
    app.run(debug=environ.get('DEBUG', False), threaded=False, use_reloader=True, host='0.0.0.0')