from app import db

# Alist common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship


class UserAccount(Model):
    ''' Account model for storing credit account related data '''

    user_id = Column(db.Integer, db.ForeignKey('user.id'))
    account_id = Column(db.Integer, db.ForeignKey('account.id'))
    PrimaryKeyConstraint(user_id, account_id, name='user_account_pk')
