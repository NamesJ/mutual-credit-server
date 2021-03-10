from app import db

from datetime import datetime

# Aliias common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


class Offer(Model):
    id = Column(db.Integer, primary_key=True)
    seller = Column(db.Integer, db.ForeignKey('user.id'))
    title = Column(db.String(128))
    price = Column(db.Integer)
    description=Column(db.String(4000))
    created_on = Column(db.DateTime, default=datetime.utcnow)
