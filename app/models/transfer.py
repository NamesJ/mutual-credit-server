from datetime import datetime
from app import db, bcrypt

# Alias common DB names
Column = db.Column
Model = db.Model


class Transfer(Model):
    ''' Transfer model for storing transfer related data '''
    __tablename__ = 'transfers'

    id = Column(db.Integer, primary_key=True)
    sender = Column(db.Integer, db.ForeignKey('user.id'))
    receiver = Column(db.Integer, db.ForeignKey('user.id'))
    value = Column(db.Integer)
    memo = Column(db.String(100))
    status = Column(db.String)
    opened_on = Column(db.DateTime, default=datetime.utcnow)
    closed_on = Column(db.DateTime)

    def __init__(self, **kwargs):
        super(Transfer, self).__init__(**kwargs)
