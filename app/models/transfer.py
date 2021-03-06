from datetime import datetime
from app import db, bcrypt

# Alias common DB names
Column = db.Column
Model = db.Model


class Transfer(Model):
    ''' Transfer model for storing transfer related data '''

    id = Column(db.Integer, primary_key=True)
    sender = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver = Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    value = Column(db.Integer, nullable=False)
    memo = Column(db.String(100), nullable=False, default='')
    status = Column(db.String, nullable=False, server_default='PENDING')
    opened_on = Column(db.DateTime, nullable=False, default=datetime.utcnow())
    closed_on = Column(db.DateTime)

    def __init__(self, **kwargs):
        super(Transfer, self).__init__(**kwargs)
