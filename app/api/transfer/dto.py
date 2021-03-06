from flask_restx import Namespace, fields


class TransferDto:

    api = Namespace('transfer', description='Transfer related operations.')
    transfer = api.model(
        'Transfer object',
        {
            'sender': fields.String, # send back username instead of id
            'receiver': fields.String, # send back username instead of id
            'value': fields.Integer,
            'memo': fields.String,
            'status': fields.String,
            'opened_on': fields.DateTime,
            'closed_on': fields.DateTime,
        },
    )

    transfer_search_success = api.model(
        'Transfers search response data',
        {
            'status': fields.Boolean,
            'message': fields.String,
            'transfers': fields.List(fields.Nested(transfer)),
        },
    )

    transfer_create = api.model(
        "Transfer create data",
        {
            'receiver': fields.String, # receiver username
            'value': fields.Integer,
            'memo': fields.String,
        },
    )

    transfer_create_success = api.model(
        'Transfer create success response',
        {
            "status": fields.Boolean,
            "message": fields.String,
            "transfer": fields.Nested(transfer),
        }
    )
