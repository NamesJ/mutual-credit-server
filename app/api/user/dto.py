from flask_restx import Namespace, fields


class UserDto:

    api = Namespace("user", description="User related operations.")
    account = api.model(
        'Account object',
        {
            'id': fields.Integer,
            'balance': fields.Integer,
            'allowance': fields.Integer,
            'created_on': fields.DateTime,
        }
    )

    user = api.model(
        "User object",
        {
            "accounts": fields.List(fields.Nested(account))
            "email": fields.String,
            "name": fields.String,
            "username": fields.String,
            "joined_date": fields.DateTime,
            "role_id": fields.Integer,
        },
    )

    data_resp = api.model(
        "User Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "user": fields.Nested(user),
        },
    )
