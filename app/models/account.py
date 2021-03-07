from app import db

import os

'''

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
'''

# Alist common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


class Account(Model):
    ''' Account model for storing credit account related data '''

    id = Column(db.Integer, primary_key=True)
    balance = Column(db.Integer, default=0, nullable=False)
    allowance = Column(
        db.Integer,
        default=os.getenv('MCS_DEFAULT_ACCOUNT_ALLOWANCE') or 200,
        nullable=False
    )
