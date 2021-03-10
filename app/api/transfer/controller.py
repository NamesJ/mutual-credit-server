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


api = TransferDto.api
transfer_search_success = TransferDto.transfer_search_success
transfer_success = TransferDto.transfer_success

transfer_create_schema = TransferCreateSchema()
transfer_get_schema = TransferGetSchema()
transfer_search_schema = TransferSearchSchema()
transfer_status_update_schema = TransferStatusUpdateSchema()


@api.route('')
class Transfer(Resource):
    ''' Transfer endpoint
    User creates transfer then receives transfer information
    User sends transfer ID to get transfer information
    '''

    transfer_create = TransferDto.transfer_create
    transfer_get = TransferDto.transfer_get
    transfer_status_update = TransferDto.transfer_status_update

    @api.doc(
        'Get a specific transfer',
        responses={
            200: ('Transfer data successfully sent', transfer_success),
            400: 'Validations failed.',
            404: 'Transfer not found!',
        },
    )
    @api.expect(transfer_get, validate=True)
    @jwt_required()
    def get(self):
        ''' Get a transfer by ID '''
        data = request.get_json()

        # Validate data
        if (errors := transfer_get_schema.validate(data)):
            return validation_error(False, errors), 400

        return TransferService.get_transfer_data(data)


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
        data = request.get_json()

        # Validate data
        if (errors := transfer_create_schema.validate(data)):
            return validation_error(False, errors), 400

        return TransferService.create_transfer(data)


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
        data = request.get_json()

        # Validate data
        if (errors := transfer_status_update_schema.validate(data)):
            return validation_error(False, errors), 400

        return TransferService.update_transfer_status(data)



@api.route('/search')
class TransferSearch(Resource):
    ''' Transfers search endpoint
    User provides search terms then receives transfers data
    '''

    @api.doc(
        "Transfer search",
        responses={
            200: ("Search succeeded", transfer_search_success),
            400: 'Validation failed',
            404: "Transfers not found!",
        },
    )
    @jwt_required()
    def get(self):
        ''' Get one or more transfer's data by attributes '''
        data = request.get_json()

        return TransferService.search_transfers_data(data)
