#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Mika

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from secrets import token_hex
from re import match
from os import environ
from lib.database import db, Vaults, VaultEntries, create_admin_vault

app = Flask(__name__)
app.config['SECRET_KEY'] = token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaults.db'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri="memory://",
)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    create_admin_vault()

@login_manager.user_loader
def load_vault(vault_id):
    return Vaults.query.get(vault_id)

@app.before_request
def nonce():
    app.jinja_env.globals['nonce'] = token_hex(32)

@app.after_request
def security_headers(response):
    nonce = app.jinja_env.globals['nonce']
    response.headers['Content-Security-Policy'] = f"base-uri 'none'; script-src 'strict-dynamic' 'nonce-{nonce}' 'unsafe-inline' https: http: ; base-uri 'none'; child-src 'none'; connect-src 'self'; font-src 'self'; form-action 'self'; frame-ancestors 'none'; frame-src 'none'; style-src 'nonce-{nonce}'; object-src 'none';"
    return response

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/vaults', methods=['GET'])
def vaults():
    if current_user.is_authenticated:
        return redirect(url_for('vault'))

    vaults = Vaults.query.with_entities(Vaults.id, Vaults.name, Vaults.is_paying_customer).order_by(Vaults.id.asc()).all()
    return render_template('vaults.html', vaults=vaults)

@app.route('/vault', methods=['GET'])
@login_required
def vault():
    vault_id = current_user.id
    vault = Vaults.query.get(vault_id)
    entries = VaultEntries.query.filter_by(vault_id=vault_id).all()

    return render_template('vault.html', vault=vault, entries=entries)

@app.route('/create', methods=['POST'])
def create():
    if not request.form['vaultName'] or not request.form['pinCode']:
        flash("Tous les champs sont requis", "error")
        return redirect(url_for('vaults'))

    if Vaults.query.filter_by(name=request.form['vaultName']).first():
        flash("Ce nom de coffre existe déjà", "error")
        return redirect(url_for('vaults'))

    vault = Vaults(name=request.form['vaultName'])

    if not match(r'^[0-9]{4,10}$', request.form['pinCode']):
        flash("Le code PIN doit faire entre 4 et 10 digits", "error")
        return redirect(url_for('vaults'))

    vault.set_pin_code(request.form['pinCode'])

    db.session.add(vault)
    db.session.commit()

    flash("Coffre créé avec succès !", "success")
    return redirect(url_for('vaults'))

@app.route('/unlock', methods=['POST'])
@limiter.limit("10 per minute")
def unlock():
    if not request.form['vaultId'] or not request.form['pinCode']:
        flash("Tous les champs sont requis !", "error")
        return redirect(url_for('vaults'))

    if not Vaults.query.filter_by(id=request.form['vaultId']):
        flash("Ce coffre n'existe pas.", "error")
        return redirect(url_for('vaults'))
    
    vault = Vaults.query.get(request.form['vaultId'])

    if not vault.check_pin_code(request.form['pinCode']):
        flash("Code PIN invalide !", "error")
        return redirect(url_for('vaults'))

    login_user(vault)
    flash("Coffre dévérrouillé avec succès", "success")
    return redirect(url_for('vault'))

@app.route('/delete', methods=['GET'])
@login_required
def delete():
    vault_id = current_user.id
    vault = Vaults.query.get(vault_id)

    if vault.id == 1:
        flash("Vous ne pouvez pas supprimer ce coffre !", "error")
        return redirect(url_for('vaults'))

    db.session.delete(vault)
    db.session.query(VaultEntries).filter_by(vault_id=vault_id).delete()
    
    db.session.commit()

    flash("Coffre supprimé avec succès !", "success")
    return redirect(url_for('vaults'))

@app.route('/lock', methods=['GET'])
@login_required
def lock():
    logout_user()
    flash("Coffre verrouillé avec succès !", "success")
    return redirect(url_for('vaults'))

@app.route('/add_entry', methods=['POST'])
@login_required
def add_entry():
    if not request.form['entryType'] or not request.form['entryValue']:
        flash("Tous les champs sont requis !", "error")
        return redirect(url_for('vault'))

    vault_id = current_user.id
    vault = Vaults.query.get(vault_id)

    entry = VaultEntries(
        vault_id=vault_id,
        entry_type=request.form['entryType'],
        value=request.form['entryValue'],
        note=request.form['entryNote']
    )

    db.session.add(entry)
    db.session.commit()

    flash("Entrée ajoutée avec succès !", "success")
    return redirect(url_for('vault', vault_id=vault_id))

@app.route('/delete_entry', methods=['GET'])
@login_required
def delete_entry():
    if not request.args.get('entry_id'):
        flash("Entrée invalide !", "error")
        return redirect(url_for('vault'))

    vault_id = current_user.id
    entry_id = request.args.get('entry_id')
    entry = VaultEntries.query.get(entry_id)

    if entry.vault_id != vault_id:
        flash("Vous ne pouvez pas supprimer cette entrée !", "error")
        return redirect(url_for('vault', vault_id=vault_id))

    if entry.entry_type == "FLAG":
        flash("Vous ne pouvez pas supprimer cette entrée !", "error")
        return redirect(url_for('vault', vault_id=vault_id))

    db.session.delete(entry)
    db.session.commit()

    flash("Entrée supprimée avec succès !", "success")
    return redirect(url_for('vault', vault_id=vault_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=environ.get('DEBUG', False), threaded=False)