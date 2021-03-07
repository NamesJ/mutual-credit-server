from app import config
from app import db


# Alist common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


class Account(Model):
    ''' Account model for storing credit account related data '''

    id = Column(db.Integer, primary_key=True)
    balance = Column(db.Integer, server_default=0, nullable=False)
    allowance = Column(db.Integer, default=app.config['MCS_DEFAULT_ACCOUNT_ALLOWANCE'])
