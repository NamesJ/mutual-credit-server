from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.utils import validation_error

from .service import TransferService
from .dto import TransferDto
from .utils import (
    TransferCreateSchema,
    TransferGetSchema,
    TransferSearchSchema,
    TransferStatusUpdateSchema
)

transfer_create_schema = TransferCreateSchema()
transfer_get_schema = TransferGetSchema()
transfer_search_schema = TransferSearchSchema()
transfer_status_update_schema = TransferStatusUpdateSchema()

api = TransferDto.api
transfer_search_success = TransferDto.transfer_search_success
transfer_success = TransferDto.transfer_success


@api.route('')
class TransferCreate(Resource):
    ''' Transfer create endpoint
    User creates transfer then receives transfer information
    '''

    transfer_create = TransferDto.transfer_create
    transfer_status_update = TransferDto.transfer_status_update

    @api.doc(

    )
    @jwt_required()
    def get(self):
        ''' Get a transfer by ID '''
        transfer_data = request.get_json()

        # Validate data
        if (errors := transfer_get_schema.validate(transfer_data)):
            return validation_error(False, errors), 400

        return TransferService.get_transfer_data(transfer_data)


    @api.doc(
        "Transfer create",
        responses={
            200: ("Transfer created", transfer_success),
            400: "Validations failed.",
            404: "Username does not match any account.",
        },
    )
    @api.expect(transfer_create, validate=True)
    @jwt_required()
    def post(self):
        ''' Initiate a new transfer '''
        # Grab the json data
        transfer_data = request.get_json()

        # Validate data
        if (errors := transfer_create_schema.validate(transfer_data)):
            return validation_error(False, errors), 400

        return TransferService.create_transfer(transfer_data)


    @api.doc(
        ''' Transfer approve, cancel, deny ''',
        responses={
            200: ('Transfer updated', transfer_success),
            400: 'Validations failed',
            404: 'Bad/non-existant user, status, authorization.',
        }
    )
    @api.expect(transfer_status_update, validate=True)
    @jwt_required()
    def put(self):
        ''' Update the status of an existing transfer '''
        transfer_data = request.get_json()

        # Validate data
        if (errors := transfer_status_update_schema.validate(transfer_data)):
            return validation_error(False, errors), 400

        return TransferService.update_transfer_status(transfer_data)



@api.route('/search')
class TransferSearch(Resource):
    ''' Transfers search endpoint
    User provides search terms then receives transfers data
    '''

    transfer_obj = TransferDto.transfer

    @api.doc(
        "Transfer search",
        responses={
            200: ("Search succeeded", transfer_search_success),
            404: "Transfers not found!",
        },
    )
    @api.expect(transfer_obj, validate=True)
    @jwt_required()
    def get(self):
        ''' Get one or more transfer's data by attributes '''
        search_data = request.get_json()

        # Validate data
        if (errors := transfer_search_schema.validate(search_data)):
            return validation_error(False, errors), 400

        return TransferService.search_transfers_data(search_data)
