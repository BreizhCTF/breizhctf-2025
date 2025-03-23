#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Mika

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ 

db = SQLAlchemy()

class Vaults(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    pin_code = db.Column(db.String(25), nullable=False)
    is_paying_customer = db.Column(db.Boolean, default=False)

    def set_pin_code(self, pin_code):
        self.pin_code = generate_password_hash(pin_code)
 
    def check_pin_code(self, pin_code):
        return check_password_hash(self.pin_code, pin_code)

class VaultEntries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vault_id = db.Column(db.Integer, db.ForeignKey('vaults.id'), nullable=False)
    entry_type = db.Column(db.String(), nullable=False)
    value = db.Column(db.String(), nullable=False)
    note = db.Column(db.String(), nullable=True)

def create_admin_vault():
    if Vaults.query.filter_by(name="My Super Secret Admin Vault").first():
        return
   
    vault = Vaults(name="My Super Secret Admin Vault", is_paying_customer=True)
    vault.set_pin_code(environ.get("VAULT_PIN", "1234"))
    db.session.add(vault)
    db.session.commit()

    admin_vault = Vaults.query.filter_by(name="My Super Secret Admin Vault").first()

    entry = VaultEntries(
        vault_id=admin_vault.id, 
        entry_type="FLAG", value=environ.get("FLAG", "BZHCTF{PLACEHOLDER_FLAG}"), 
        note="Well done! You pwned my vault app >:("
    )

    db.session.add(entry)
    db.session.commit()
