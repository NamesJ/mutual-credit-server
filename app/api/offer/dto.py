from flask_restx import Namespace, fields


class OfferDto:

    api = Namespace('offer', description='Offer related operations.')
    offer = api.model(
        'Offer data',
        {
            'id': fields.Integer,
            'seller': fields.String, # send back username instead of id
            'title': fields.String,
            'price': fields.Integer,
            'description': fields.String,
            'created_on': fields.DateTime,
        },
    )

    offer_delete_success = api.model(
        'Offer delete success response data',
        {
            'status': fields.Boolean,
            'message': fields.String,
        }
    )

    offer_success = api.model(
        'Offer get/create/put success response data',
        {
            'status': fields.Boolean,
            'message': fields.String,
            'offer': fields.Nested(offer),
        }
    )

    offer_delete = api.model(
        'Offer delete input data',
        {
            'id': fields.Integer
        }
    )

    offer_create = api.model(
        'Offer create input data',
        {
            'title': fields.String, # receiver username
            'price': fields.Integer,
            'description': fields.String,
        },
    )

    offer_get = api.model(
        'Offer get input data',
        {
            'id': fields.Integer,
        },
    )

    offer_update = api.model(
        'Offer update input data',
        {
            'id': fields.Integer,
            'changes': fields.Nested(offer_create),
        }
    )
