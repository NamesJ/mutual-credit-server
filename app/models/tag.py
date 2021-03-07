from app import db

# Alias common DB names
Column = db.Column
Model = db.Model


class Tag(Model):
    ''' Tag model for storing entity tag related data '''

    entity_type = Column(db.String(30), primary_key=True)
    entity_value = Column(db.String(128), primary_key=True)
    tag = Column(db.String(100), primary_key=True)

    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
