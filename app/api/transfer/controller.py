from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from app.utils import validation_error

from .service import TransferService
from .dto import TransferDto
from .utils import TransferCreateSchema, TransferSearchSchema

transfer_create_schema = TransferCreateSchema()
transfer_search_schema = TransferSearchSchema()

api = TransferDto.api
transfer_search_success = TransferDto.transfer_search_success
transfer_create_success = TransferDto.transfer_create_success


@api.route('/create')
class TransferCreate(Resource):
    ''' Transfer create endpoint
    User creates transfer then receives transfer information
    '''

    transfer_create = TransferDto.transfer_create

    @api.doc(
        "Transfer create",
        responses={
            200: ("Transfer created", transfer_create_success),
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



@api.route('/search')
class TransferSearch(Resource):
    ''' Transfers search endpoint
    User provides search terms then receives transfers data
    '''

    @api.doc(
        "Transfer search",
        responses={
            200: ("Search succeeded", transfer_search_success),
            404: "Transactions not found!",
        },
    )
    @jwt_required()
    def get(self):
        ''' Get one or more transfer's data by attributes '''
        search_data = request.get_json()

        # Validate data
        if (errors := transfer_search_schema.validate(search_data)):
            return validation_error(False, errors), 400

        return TransferService.get_transfers_data(search_data)
