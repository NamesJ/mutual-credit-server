# Model Schemas
from app import ma

from .user import User
from .transfer import Transfer



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("allowance", "balance", "email", "name", "username",
                  "joined_date", "role_id")


class OfferSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'seller', 'title', 'price', 'description', 'created_on')


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('entity_type', 'entity_value', 'tag')


class TransferSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'sender', 'receiver', 'value', 'memo', 'status',
                  'opened_on', 'closed_on')
