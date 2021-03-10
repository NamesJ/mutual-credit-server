from app import db
from app.models.user import User
from app.models.transfer import Transfer

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user

from flask_jwt_extended import create_access_token
import itertools
import json



def create_transfer(self, access_token, data):
    return self.client.post(
        f'/api/transfer',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps(data)
    )


def update_transfer_status(self, access_token, id, status):
    return self.client.put(
        f'/api/transfer',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps({ 'action': status, 'id': id })
    )


def get_transfer_data(self, access_token, id):
    return self.client.get(
        f'/api/transfer',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps({ 'id': id })
    )


def search_transfers_data(self, access_token, payload):
    return self.client.get(
        '/api/transfer/search',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps(payload)
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
        payload = {
            'receiver': bobby_username,
            'value': 7
        }

        transfer_response = create_transfer(self, alice_access_token, payload)
        transfer_data = json.loads(transfer_response.data.decode())

        self.assertTrue(transfer_response.status)
        self.assertEqual(transfer_response.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], alice_username)
        self.assertEqual(transfer_data['transfer']['receiver'], payload['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], payload['value'])
        self.assertEqual(transfer_data['transfer']['memo'], '')
        self.assertEqual(transfer_data['transfer']['status'], 'PENDING')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])


        # Bobby creates transfer to Alice
        payload = {
            'receiver': 'alice',
            'value': 45,
            'memo': 'baking supplies'
        }
        transfer_response = create_transfer(self, bobby_access_token, payload)
        transfer_data = json.loads(transfer_response.data.decode())

        self.assertTrue(transfer_response.status)
        self.assertEqual(transfer_response.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], bobby_username)
        self.assertEqual(transfer_data['transfer']['receiver'], payload['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], payload['value'])
        self.assertEqual(transfer_data['transfer']['memo'], payload['memo'])
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
        sender = alice_username
        receiver = bobby_username
        value=45
        memo='baking supplies'
        transfer = Transfer(sender=alice.id, receiver=bobby.id, value=value,
                            memo=memo)

        db.session.add(transfer)
        db.session.commit()

        transfer_response = get_transfer_data(self, alice_access_token, transfer.id)
        transfer_data = json.loads(transfer_response.data.decode())

        self.assertTrue(transfer_response.status)
        self.assertEqual(transfer_response.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], sender)
        self.assertEqual(transfer_data['transfer']['receiver'], receiver)
        self.assertEqual(transfer_data['transfer']['value'], value)
        self.assertEqual(transfer_data['transfer']['memo'], memo)
        self.assertEqual(transfer_data['transfer']['status'], 'PENDING')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        alice_balance_before = alice.balance
        bobby_balance_before = bobby.balance

        # Bobby approves the transfer from Alice
        approve_response = update_transfer_status(self, bobby_access_token,
                                    transfer_data['transfer']['id'], 'approve')
        approve_data = json.loads(approve_response.data.decode())

        # Check for expected changes
        self.assertEqual(transfer_data['transfer']['sender'], approve_data['transfer']['sender'])
        self.assertEqual(transfer_data['transfer']['receiver'], approve_data['transfer']['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], approve_data['transfer']['value'])
        self.assertEqual(transfer_data['transfer']['memo'], approve_data['transfer']['memo'])
        self.assertNotEqual(transfer_data['transfer']['status'], approve_data['transfer']['status'])
        self.assertEqual(transfer_data['transfer']['opened_on'], approve_data['transfer']['opened_on'])
        self.assertNotEqual(transfer_data['transfer']['closed_on'], approve_data['transfer']['closed_on'])

        self.assertEqual(alice.balance, alice_balance_before - value)
        self.assertEqual(bobby.balance, alice_balance_before + value)

        # Check new values for transfer are as expected
        self.assertTrue(approve_response.status)
        self.assertEqual(approve_response.status_code, 200)
        self.assertEqual(approve_data['transfer']['sender'], sender)
        self.assertEqual(approve_data['transfer']['receiver'], receiver)
        self.assertEqual(approve_data['transfer']['value'], value)
        self.assertEqual(approve_data['transfer']['memo'], memo)
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

        access_token = create_access_token(identity=alice.id)

        bobby_username = 'bobby'
        bobby = User(username=bobby_username)

        db.session.add(bobby)
        db.session.commit()

        # Alice creates transfer to Bobby
        sender = alice_username
        receiver = bobby_username
        value=45
        memo='baking supplies'
        transfer = Transfer(sender=alice.id, receiver=bobby.id, value=value,
                            memo=memo)

        db.session.add(transfer)
        db.session.commit()

        transfer_response = get_transfer_data(self, access_token, transfer.id)
        transfer_data = json.loads(transfer_response.data.decode())

        self.assertTrue(transfer_response.status)
        self.assertEqual(transfer_response.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], sender)
        self.assertEqual(transfer_data['transfer']['receiver'], receiver)
        self.assertEqual(transfer_data['transfer']['value'], value)
        self.assertEqual(transfer_data['transfer']['memo'], memo)
        self.assertEqual(transfer_data['transfer']['status'], 'PENDING')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        # Alice cancels the transfer
        cancel_response = update_transfer_status(self, access_token,
                                    transfer_data['transfer']['id'], 'cancel')
        cancel_data = json.loads(cancel_response.data.decode())

        # Check for expected changes
        self.assertEqual(transfer_data['transfer']['sender'], cancel_data['transfer']['sender'])
        self.assertEqual(transfer_data['transfer']['receiver'], cancel_data['transfer']['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], cancel_data['transfer']['value'])
        self.assertEqual(transfer_data['transfer']['memo'], cancel_data['transfer']['memo'])
        self.assertNotEqual(transfer_data['transfer']['status'], cancel_data['transfer']['status'])
        self.assertEqual(transfer_data['transfer']['opened_on'], cancel_data['transfer']['opened_on'])
        self.assertNotEqual(transfer_data['transfer']['closed_on'], cancel_data['transfer']['closed_on'])

        # Check for expected values
        self.assertTrue(cancel_response.status)
        self.assertEqual(cancel_response.status_code, 200)
        self.assertEqual(cancel_data['transfer']['sender'], sender)
        self.assertEqual(cancel_data['transfer']['receiver'], receiver)
        self.assertEqual(cancel_data['transfer']['value'], value)
        self.assertEqual(cancel_data['transfer']['memo'], memo)
        self.assertEqual(cancel_data['transfer']['status'], 'CANCELLED')
        self.assertIsNotNone(cancel_data['transfer']['opened_on'])
        self.assertIsNotNone(cancel_data['transfer']['closed_on'])

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

        db.session.add(bobby)
        db.session.commit()

        bobby_access_token = create_access_token(identity=bobby.id)

        # Alice creates transfer to Bobby
        sender = alice_username
        receiver = bobby_username
        value=45
        memo='baking supplies'
        transfer = Transfer(sender=alice.id, receiver=bobby.id, value=value,
                            memo=memo)

        db.session.add(transfer)
        db.session.commit()

        transfer_response = get_transfer_data(self, alice_access_token, transfer.id)
        transfer_data = json.loads(transfer_response.data.decode())

        self.assertTrue(transfer_response.status)
        self.assertEqual(transfer_response.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], sender)
        self.assertEqual(transfer_data['transfer']['receiver'], receiver)
        self.assertEqual(transfer_data['transfer']['value'], value)
        self.assertEqual(transfer_data['transfer']['memo'], memo)
        self.assertEqual(transfer_data['transfer']['status'], 'PENDING')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        # Bobby denies the transfer from Alice
        deny_response = update_transfer_status(self, bobby_access_token,
                                        transfer_data['transfer']['id'], 'deny')
        deny_data = json.loads(deny_response.data.decode())

        # Check for expected changes
        self.assertEqual(transfer_data['transfer']['sender'], deny_data['transfer']['sender'])
        self.assertEqual(transfer_data['transfer']['receiver'], deny_data['transfer']['receiver'])
        self.assertEqual(transfer_data['transfer']['value'], deny_data['transfer']['value'])
        self.assertEqual(transfer_data['transfer']['memo'], deny_data['transfer']['memo'])
        self.assertNotEqual(transfer_data['transfer']['status'], deny_data['transfer']['status'])
        self.assertEqual(transfer_data['transfer']['opened_on'], deny_data['transfer']['opened_on'])
        self.assertNotEqual(transfer_data['transfer']['closed_on'], deny_data['transfer']['closed_on'])

        # Check for expected values
        self.assertTrue(deny_response.status)
        self.assertEqual(deny_response.status_code, 200)
        self.assertEqual(deny_data['transfer']['sender'], alice_username)
        self.assertEqual(deny_data['transfer']['receiver'], receiver)
        self.assertEqual(deny_data['transfer']['value'], value)
        self.assertEqual(deny_data['transfer']['memo'], memo)
        self.assertEqual(deny_data['transfer']['status'], 'DENIED')
        self.assertIsNotNone(deny_data['transfer']['opened_on'])
        self.assertIsNotNone(deny_data['transfer']['closed_on'])

        db.session.remove()


    def test_transfer_get(self):
        ''' Test getting a transfer '''
        # Create two new mock users
        alice_username = 'alice'
        alice = User(username=alice_username)

        db.session.add(alice)
        db.session.commit()

        access_token = create_access_token(identity=alice.id)

        bobby_username = 'bobby'
        bobby = User(username=bobby_username)

        db.session.add(bobby)
        db.session.commit()

        # Alice creates transfer to Bobby
        sender = alice_username
        receiver = bobby_username
        value=45
        memo='baking supplies'
        transfer = Transfer(sender=alice.id, receiver=bobby.id, value=value,
                            memo=memo)

        db.session.add(transfer)
        db.session.commit()

        transfer_response = get_transfer_data(self, access_token, transfer.id)
        transfer_data = json.loads(transfer_response.data.decode())

        self.assertTrue(transfer_response.status)
        self.assertEqual(transfer_response.status_code, 200)
        self.assertEqual(transfer_data['transfer']['sender'], sender)
        self.assertEqual(transfer_data['transfer']['receiver'], receiver)
        self.assertEqual(transfer_data['transfer']['value'], value)
        self.assertEqual(transfer_data['transfer']['memo'], memo)
        self.assertEqual(transfer_data['transfer']['status'], 'PENDING')
        self.assertIsNotNone(transfer_data['transfer']['opened_on'])
        self.assertIsNone(transfer_data['transfer']['closed_on'])

        db.session.remove()


    def test_transfer_search(self):
        ''' Test get transfers by search '''
        # Create two new mock users
        alice_username = 'alice'
        alice = User(username=alice_username)

        db.session.add(alice)
        db.session.commit()

        access_token = create_access_token(identity=alice.id)

        bobby_username = 'bobby'
        bobby = User(username=bobby_username)

        db.session.add(bobby)
        db.session.commit()

        # Alice creates transfer to Bobby
        sender = alice_username
        receiver = bobby_username
        value=45
        memo='baking supplies'
        transfer0 = Transfer(sender=alice.id, receiver=bobby.id, value=value,
                            memo=memo)

        db.session.add(transfer0)
        db.session.commit()

        transfer_info = {
            'id': transfer0.id,
            'sender': alice_username,
            'receiver': bobby_username,
            'status': transfer0.status,
            'value': transfer0.value,
            'memo': transfer0.memo
        }


        all_combinations = []

        # all combinations of key-value pairs
        for num_pairs in range(1, len(transfer_info)-1):
            cmbs = list(map(dict,itertools.combinations(transfer_info.items(),
                                                        num_pairs)))
            all_combinations.append(cmbs)

        # search all combinations
        for cmb in all_combinations:
            payload = {}

            for d in cmb:
                payload.update(d)

            transfers_response = search_transfers_data(self, access_token,
                                                       payload)
            transfers_data = json.loads(transfers_response.data.decode())

            self.assertTrue(transfers_response.status)
            self.assertEqual(transfers_response.status_code, 200)
            #self.assertEqual(len(transfers_data['transfers']), 2)

            for transfer_data in transfers_data['transfers']:
                self.assertEqual(transfer_data['sender'], sender)
                self.assertEqual(transfer_data['receiver'], receiver)
                self.assertEqual(transfer_data['value'], value)
                self.assertEqual(transfer_data['memo'], memo)
                self.assertEqual(transfer_data['status'], 'PENDING')
                self.assertIsNotNone(transfer_data['opened_on'])
                self.assertIsNone(transfer_data['closed_on'])

        # search for value that doesn't exist in DB
        payload = {
            'sender': 'sender.username.that.does.not.exist'
        }

        transfers_response = search_transfers_data(self, access_token, payload)
        transfers_data = json.loads(transfers_response.data.decode())

        self.assertTrue(transfers_response.status)
        self.assertEqual(transfers_response.status_code, 404)


        db.session.remove()
