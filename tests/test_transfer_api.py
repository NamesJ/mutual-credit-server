import json

from flask_jwt_extended import create_access_token

from app import db
from app.models.user import User
from app.models.transfer import Transfer

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user


def approve_transfer(self, access_token, transfer_id):
    return self.client.put(
        f'/api/transfer/approve',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data={ 'id': transfer_id }
    )


def cancel_transfer(self, access_token, transfer_id):
    return self.client.put(
        f'/api/transfer/cancel',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data={ 'id': transfer_id }
    )


def create_transfer(self, access_token, data):
    return self.client.post(
        f'/api/transfer/create',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps(data)
    )


def deny_transfer(self, access_token, transfer_id):
    return self.client.put(
        f'/api/transfer/deny',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data={ 'id': transfer_id }
    )


def get_transfers_data(self, access_token, data):
    return self.client.get(
        f'/api/transfer/search',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=data
    )


class TestTransferBlueprint(BaseTestCase):
    def test_transfer_create(self):
        ''' Test creating a transfer in DB '''

        # Create two mock users
        alice_username = 'alice'
        alice = User(username=alice_username)

        db.session.add(alice)
        db.session.commit()

        alice_access_token = create_access_token(identity=alice.id)

        bobby_username = 'bobby'
        bobby = User(username=bobby_username)

        db.session.add(bobby)
        db.session.commit()

        bobby_access_token = create_access_token(identity=bobby.id)

        # Alice creates transfer to Bobby
        t_info = {
            'receiver': 'bobby',
            'value': 7
        }
        transfer_resp = create_transfer(self, alice_access_token, t_info)
        transfer_data = json.loads(transfer_resp.data.decode())

        self.assertTrue(transfer_resp.status)
        self.assertEqual(transfer_resp.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], alice_username)
        self.assertEqual(transfer_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], t_info['value'])
        self.assertEqual(transfer_data['transfer']['memo'], '')
        self.assertEqual(transfer_data['transfer']['status'], 'PENDING')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])


        # Bobby creates transfer to Alice
        t_info = {
            'receiver': 'alice',
            'value': 45,
            'memo': 'baking supplies'
        }
        transfer_resp = create_transfer(self, bobby_access_token, t_info)
        transfer_data = json.loads(transfer_resp.data.decode())

        self.assertTrue(transfer_resp.status)
        self.assertEqual(transfer_resp.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], bobby_username)
        self.assertEqual(transfer_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], t_info['value'])
        self.assertEqual(transfer_data['transfer']['memo'], t_info['memo'])
        self.assertEqual(transfer_data['transfer']['status'], 'PENDING')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        #self.assertTrue(False)

        db.session.remove()


    def test_transfer_approve(self):
        ''' Test approving a transfer '''
        # Create two new mock users
        alice_username = 'alice'
        alice = User(username=alice_username)

        db.session.add(alice)
        db.session.commit()

        alice_access_token = create_access_token(identity=alice.id)

        bobby_username = 'bobby'
        bobby = User(username=bobby_username)

        db.session.add(bobby)
        db.session.commit()

        bobby_access_token = create_access_token(identity=bobby.id)

        # Alice creates transfer to Bobby
        t_info = {
            'receiver': 'bobby',
            'value': 45,
            'memo': 'baking supplies'
        }
        transfer_resp = create_transfer(self, alice_access_token, t_info)
        transfer_data = json.loads(transfer_resp.data.decode())

        # Check transfer values are as expected
        self.assertTrue(transfer_resp.status)
        self.assertEqual(transfer_resp.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], alice_username)
        self.assertEqual(transfer_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], t_info['value'])
        self.assertEqual(transfer_data['transfer']['memo'], t_info['memo'])
        self.assertEqual(transfer_data['transfer']['status'], 'PENDING')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        # Bobby approves the transfer from Alice
        approve_response = approve_transfer(self, bobby_access_token, transfer_data['transfer']['id'])
        approve_data = json.loads(approve_response.data.decode())

        # Check for expected changes
        self.assertEqual(transfer_data['transfer']['sender'], approve_data['transfer']['sender'])
        self.assertEqual(transfer_data['transfer']['receiver'], approve_data['transfer']['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], approve_data['transfer']['value'])
        self.assertEqual(transfer_data['transfer']['memo'], approve_data['transfer']['memo'])
        self.assertNotEqual(transfer_data['transfer']['status'], approve_data['transfer']['status'])
        self.assertEqual(transfer_data['transfer']['opened_on'], approve_data['transfer']['opened_on'])
        self.assertNotEqual(transfer_data['transfer']['closed_on'], approve_data['transfer']['closed_on'])

        # Check new values for transfer are as expected
        self.assertTrue(approve_resp.status)
        self.assertEqual(approve_resp.status_code, 200)
        self.assertEqual(approve_data['transfer']['sender'], alice_username)
        self.assertEqual(approve_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(approve_data['transfer']['value'], t_info['value'])
        self.assertEqual(approve_data['transfer']['memo'], t_info['memo'])
        self.assertEqual(approve_data['transfer']['status'], 'APPROVED')
        self.assertIsNotNone(approve_data['transfer']['opened_on'])
        self.assertIsNotNone(approve_data['transfer']['closed_on'])

        db.session.remove()


    def test_transfer_cancel(self):
        ''' Test cancelling a transfer '''
        # Create two new mock users
        alice_username = 'alice'
        alice = User(username=alice_username)

        db.session.add(alice)
        db.session.commit()

        alice_access_token = create_access_token(identity=alice.id)

        bobby_username = 'bobby'
        bobby = User(username=bobby_username)

        db.session.add(bobby)
        db.session.commit()

        bobby_access_token = create_access_token(identity=bobby.id)

        # Alice creates transfer to Bobby
        t_info = {
            'receiver': 'bobby',
            'value': 45,
            'memo': 'baking supplies'
        }
        transfer_resp = create_transfer(self, alice_access_token, t_info)
        transfer_data = json.loads(transfer_resp.data.decode())

        self.assertTrue(transfer_resp.status)
        self.assertEqual(transfer_resp.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], alice_username)
        self.assertEqual(transfer_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], t_info['value'])
        self.assertEqual(transfer_data['transfer']['memo'], t_info['memo'])
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        # Alice cancels the transfer
        cancel_response = cancel_transfer(self, alice_access_token, None)
        cancel_data = json.loads(cancel_response.data.decode())

        # TODO: Check that values that shouldn't have changed, haven't changed
        # transfer_data <--> cancel_data

        self.assertTrue(cancel_response.status)
        self.assertEqual(cancel_response.status_code, 200)
        self.assertEqual(cancel_data['transfer']['sender'], alice_username)
        self.assertEqual(cancel_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(cancel_data['transfer']['value'], t_info['value'])
        self.assertEqual(cancel_data['transfer']['memo'], t_info['memo'])
        self.assertEqual(cancel_data['transfer']['status'], 'CANCELLED')
        self.assertIsNotNone(cancel_data['transfer']['opened_on'])
        self.assertIsNotNone(cancel_data['transfer']['closed_on'])

        self.assertTrue(False)

        db.session.remove()


    def test_transfer_deny(self):
        ''' Test denying a transfer '''
        # Create two new mock users
        alice_username = 'alice'
        alice = User(username=alice_username)

        db.session.add(alice)
        db.session.commit()

        alice_access_token = create_access_token(identity=alice.id)

        bobby_username = 'bobby'
        bobby = User(username=bobby_username)

        bobby_access_token = create_access_token(identity=bobby.id)

        db.session.add(bobby)
        db.session.commit()

        # Alice creates transfer to Bobby
        t_info = {
            'receiver': 'bobby',
            'value': 45,
            'memo': 'baking supplies'
        }
        transfer_resp = create_transfer(self, alice_access_token, t_info)
        transfer_data = json.loads(transfer_resp.data.decode())

        self.assertTrue(transfer_resp.status)
        self.assertEqual(transfer_resp.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], alice_username)
        self.assertEqual(transfer_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], t_info['value'])
        self.assertEqual(transfer_data['transfer']['memo'], t_info['memo'])
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        # Bobby denies the transfer from Alice
        resp = deny_transfer(self, bobby_access_token, None)
        print(resp)

        self.assertTrue(False)

        db.session.remove()


    def test_transfer_get(self):
        ''' Test getting a transfer '''
        # Create two new mock users
        alice_username = 'alice'
        alice = User(username=alice_username)

        db.session.add(alice)
        db.session.commit()

        alice_access_token = create_access_token(identity=alice.id)

        bobby_username = 'bobby'
        bobby = User(username=bobby_username)

        bobby_access_token = create_access_token(identity=bobby.id)

        db.session.add(bobby)
        db.session.commit()

        # Alice creates transfer to Bobby
        t_info = {
            'receiver': 'bobby',
            'value': 45,
            'memo': 'baking supplies'
        }
        transfer_resp = create_transfer(self, alice_access_token, t_info)
        transfer_data = json.loads(transfer_resp.data.decode())

        self.assertTrue(transfer_resp.status)
        self.assertEqual(transfer_resp.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], alice_username)
        self.assertEqual(transfer_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], t_info['value'])
        self.assertEqual(transfer_data['transfer']['memo'], t_info['memo'])
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        # Alice gets pending transfer
        resp = get_transfers_data(self, alice_access_token, { 'id': None })

        # Bobby approves the transfer from Alice
        resp = approve_transfer(self, bobby_access_token, None)
        print(resp)

        # Alice gets pending transfer
        resp = get_transfers_data(self, alice_access_token, { 'id': None })

        transfer_resp = create_transfer(self, alice_access_token, t_info)
        transfer_data = json.loads(transfer_resp.data.decode())

        self.assertTrue(transfer_resp.status)
        self.assertEqual(transfer_resp.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], alice_username)
        self.assertEqual(transfer_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], t_info['value'])
        self.assertEqual(transfer_data['transfer']['memo'], '')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        # Bobby denies the transfer from Alice
        resp = deny_transfer(self, bobby_access_token, None)
        print(resp)

        # Alice gets pending transfer
        resp = get_transfers_data(self, alice_access_token, { 'id': None })


        # Alice creates a new transfer
        transfer_resp = create_transfer(self, alice_access_token, t_info)
        transfer_data = json.loads(transfer_resp.data.decode())

        self.assertTrue(transfer_resp.status)
        self.assertEqual(transfer_resp.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], alice_username)
        self.assertEqual(transfer_data['transfer']['receiver'], t_info['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], t_info['value'])
        self.assertEqual(transfer_data['transfer']['memo'], '')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        # Alice cancels the transfer
        resp = cancel_transfer(self, alice_access_token, None)
        print(resp)

        # Alice gets pending transfer
        resp = get_transfers_data(self, alice_access_token, { 'id': None })

        self.assertTrue(False)

        db.session.remove()
