# Model Schemas
from app import ma

from .user import User


class UserSchema(ma.ModelSchema):
    class Meta:
        # Fields to expose, add more if needed.
        fields = ("email", "name", "username", "joined_date", "role_id")


class TransferSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'sender', 'receiver', 'value', 'memo', 'status',
                'opened_on', 'closed_on')
