import json

from flask_jwt_extended import create_access_token

from app import db
from app.models.offer import Offer
from app.models.user import User

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user


def create_offer(self, access_token, data):
    return self.client.post(
        f'/api/offer',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps(data)
    )


def get_offer_data(self, access_token, data):
    return self.client.post(
        f'/api/offer',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps(data)
    )


def update_offer(self, access_token, data):
    return self.client.put(
        return self.client.post(
            f'/api/offer',
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='application/json',
            data=json.dumps(data)
        )
    )



class TestOfferBlueprint(BaseTestCase):
    def test_offer_create(self):
        ''' Test creating an offer in DB '''
        pass


    def test_offer_get(self):
        ''' Test getting an offer in DB '''
        pass


    def test_offer_update(self):
        ''' Test updating offer in DB '''
        pass
