from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.utils import validation_error

from .service import OfferService

from .dto import OfferDto
api = OfferDto.api
# API models for resources output
offer_success = OfferDto.offer_success
offer_delete_success = OfferDto.offer_delete_success

from .utils import (
    OfferCreateSchema,
    OfferDeleteSchema,
    OfferGetSchema,
    OfferUpdateSchema
)
# Schemas for validation of resources input
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

    # API models for resources input
    offer_delete = OfferDto.offer_delete
    offer_create = OfferDto.offer_create
    offer_get = OfferDto.offer_get
    offer_update = OfferDto.offer_update


    @api.doc(
        'Offer delete',
        responses={
            200: ('Offer data successfully sent', offer_delete_success),
            400: 'Validations failed.',
            404: 'Bad/non-existant user, status, authorization.',
        },
    )
    @api.expect(offer_delete, validate=True)
    @jwt_required()
    def delete(self):
        ''' Delete info for a specific offer '''
        data = request.get_json()

        # Validate data
        if (errors := offer_delete_schema.validate(data)):
            return validation_error(False, errors), 400

        return OfferService.delete_offer_data(data)


    @api.doc(
        'Get a specific offer',
        responses={
            200: ('Offer deleted successfully', offer_success),
            400: 'Validations failed.',
            404: 'Bad/non-existant user, status, authorization.',
        },
    )
    @api.expect(offer_get, validate=True)
    @jwt_required()
    def get(self):
        ''' Get info for a specific offer '''
        data = request.get_json()

        # Validate data
        if (errors := offer_get_schema.validate(data)):
            return validation_error(False, errors), 400

        return OfferService.get_offer_data(data)


    @api.doc(
        "Offer create",
        responses={
            200: ("Offer created", offer_success),
            400: "Validations failed.",
            404: 'Bad/non-existant user, status, authorization.',
        },
    )
    @api.expect(offer_create, validate=True)
    @jwt_required()
    def post(self):
        ''' Create an offer '''
        # Grab the json data
        data = request.get_json()

        # Validate data
        if (errors := offer_create_schema.validate(data)):
            return validation_error(False, errors), 400

        return OfferService.create_offer(data)


    @api.doc(
        ''' Update info for existing offer ''',
        responses={
            200: ('Offer updated', offer_success),
            400: 'Validations failed',
            404: 'Bad/non-existant user, status, authorization.',
        }
    )
    @api.expect(offer_update, validate=True)
    @jwt_required()
    def put(self):
        ''' Update info for a specific existing offer '''
        data = request.get_json()

        # Validate data
        if (errors := offer_update_schema.validate(data)):
            return validation_error(False, errors), 400

        return OfferService.update_offer_data(data)
