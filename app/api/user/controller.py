from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .service import UserService
from .dto import UserDto

api = UserDto.api
data_resp = UserDto.data_resp


@api.route('')
class UserGet(Resource):
    ''' User endpoint
    '''
    user_get = UserDto.user_get

    @api.doc(
        'Get a specific user',
        responses={
            200: ('User data successfully sent', data_resp),
            404: 'User not found!',
        },
    )
    @api.expect(user_get, validate=True)
    @jwt_required()
    def get(self):
        ''' Get a specific user's data by their username '''
        data = request.get_json()

        return UserService.get_user_data(data)
