import json

from flask_jwt_extended import create_access_token

from app import db
from app.models.offer import Offer
from app.models.user import User

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user


def create_offer(self, access_token, payload):
    return self.client.post(
        f'/api/offer',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps(payload)
    )


def get_offer_data(self, access_token, payload):
    return self.client.get(
        f'/api/offer',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps(payload)
    )


def update_offer_info(self, access_token, payload):
    return self.client.put(
        f'/api/offer',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps(payload)
    )



class TestOfferBlueprint(BaseTestCase):
    def test_offer_create(self):
        ''' Test creating an offer in DB '''

        # Create a mock user (seller)
        username = 'ClaustrophobicSkeleton'
        user = User(username=username)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        title = 'SpOOoOoky cake'
        price = 30
        description = '1x spOOoOoky 9x13x2in cake'

        payload = dict(title=title, price=price, description=description)

        offer_response = create_offer(self, access_token, payload)
        offer_data = json.loads(offer_response.data.decode())

        self.assertTrue(offer_response.status)
        self.assertEqual(offer_response.status_code, 200)
        self.assertIsNotNone(offer_data['offer']['id'])
        self.assertEqual(offer_data['offer']['seller'], user.username)
        self.assertEqual(offer_data['offer']['title'], title)
        self.assertEqual(offer_data['offer']['price'], price)
        self.assertEqual(offer_data['offer']['description'], description)
        # self.assertIsNotNone(offer_data['offer']['created_on'])



    def test_offer_get(self):
        ''' Test getting an offer in DB '''

        # Create a mock user (seller)
        username = 'ClaustrophobicSkeleton'
        user = User(username=username)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)
 dict(id=offer.id, title=new_title, price=new_price,
                       description=new_description)
        # Create a mock offer
        seller = username
        title = 'SpOOoOoky cake'
        price = 30
        description = '1x spOOoOoky 9x13x2in cake'
        offer = Offer(seller=seller, title=title, price=price,
                      description=description)

        db.session.add(offer)
        db.session.commit()

        payload = dict(id=offer.id)

        offer_response = get_offer_data(self, access_token, payload)
        offer_data = json.loads(offer_response.data.decode())

        self.assertTrue(offer_response.status)
        self.assertEqual(offer_response.status_code, 200)
        self.assertEqual(offer_data['offer']['id'], offer.id)
        self.assertEqual(offer_data['offer']['seller'], seller)
        self.assertEqual(offer_data['offer']['title'], title)
        self.assertEqual(offer_data['offer']['price'], price)
        self.assertEqual(offer_data['offer']['description'], description)
        #self.assertIsNotNone(offer_data['offer']['created_on'])


    def test_offer_update(self):
        ''' Test updating offer in DB '''

        # Create a mock user (seller)
        username = 'ClaustrophobicSkeleton'
        user = User(username=username)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        # Create a mock offer
        seller = username
        title = 'SpOOoOoky cake'
        price = 15
        description = '1x spOOoOoky 9x13x2in cake'
        offer = Offer(seller=seller, title=title, price=price, dict(id=offer.id, title=new_title, price=new_price,
                       description=new_description)
                      description=description)

        db.session.add(offer)
        db.session.commit()

        # Update a single value
        new_price = 30

        payload = {
            'id': offer.id,
            'changes': {
                'price': new_price
            }
        }

        offer_response = update_offer_info(self, access_token, payload)
        offer_data = json.loads(offer_response.data.decode())

        self.assertTrue(offer_response.status)
        self.assertEqual(offer_response.status_code, 200)
        self.assertEqual(offer_data['offer']['id'], offer.id)
        self.assertEqual(offer_data['offer']['seller'], seller)
        self.assertEqual(offer_data['offer']['title'], title)
        self.assertEqual(offer_data['offer']['price'], new_price)
        self.assertEqual(offer_data['offer']['description'], description)
        #self.assertIsNotNone(offer_data['offer']['created_on'])


        # Update multiple values
        new_title = 'Extra SpOOoOoky cake'
        new_price = 45
        new_description = '1x extra spOOoOoky 9x13x2in cake'

        payload ={
            'id': offer.id,
            'changes': {
                'title': new_title,
                'price': new_price,
                'description': new_description
            }
        }

        offer_response = update_offer_info(self, access_token, payload)
        offer_data = json.loads(offer_response.data.decode())

        self.assertTrue(offer_response.status)
        self.assertEqual(offer_response.status_code, 200)
        self.assertEqual(offer_data['offer']['id'], offer.id)
        self.assertEqual(offer_data['offer']['seller'], seller)
        self.assertEqual(offer_data['offer']['title'], new_title)
        self.assertEqual(offer_data['offer']['price'], new_price)
        self.assertEqual(offer_data['offer']['description'], new_description)
        #self.assertIsNotNone(offer_data['offer']['created_on'])
