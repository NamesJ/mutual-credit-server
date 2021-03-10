from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.utils import validation_error

from .service import OfferService

from .dto import OfferDto
api = OfferDto.api
offer_success = OfferDto.offer_success
offer_delete_success = OfferDto.offer_delete_success

from .utils import (
    OfferCreateSchema,
    OfferDeleteSchema,
    OfferGetSchema,
    OfferUpdateSchema
)
# Resource output schemas
offer_create_schema = OfferCreateSchema()
offer_delete_schema = OfferDeleteSchema()
offer_get_schema = OfferGetSchema()
offer_update_schema = OfferUpdateSchema()


@api.route('')
class Offer(Resource):
    ''' Offer endpoint
    DELETE: User sends offer ID and offer is deleted from DB
    GET:    User sends offer ID and receives offer info
    POST:   User creates offer then receives offer info
    PUT:    User sends offer ID name:value pairsto be updated and offer info is
            updated
    '''

    # Expected resource data models
    offer_delete = OfferDto.offer_delete
    offer_create = OfferDto.offer_create
    offer_get = OfferDto.offer_get
    offer_update = OfferDto.offer_update
