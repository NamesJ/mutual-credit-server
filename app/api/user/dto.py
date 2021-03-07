from flask_restx import Namespace, fields


class UserDto:

    api = Namespace('user', description='User related operations.')

    user_get = api.model(
        'User get object',
        {
            'username': fields.String,
        },
    )

    user = api.model(
        'User object',
        {
            'allowance': fields.Integer,
            'balance': fields.Integer,
            'email': fields.String,
            'name': fields.String,
            'username': fields.String,
            'joined_date': fields.DateTime,
            'role_id': fields.Integer,
        },
    )

    data_resp = api.model(
        'User Data Response',
        {
            'status': fields.Boolean,
            'message': fields.String,
            'user': fields.Nested(user),
        },
    )
