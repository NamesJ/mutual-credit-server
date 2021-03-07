import json

from flask_jwt_extended import create_access_token

from app import config
from app import db
from app.models.account import Account

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user


def get_account_data(self, access_token, account_id):
    return self.client.get(
        f'/api/account',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps({ 'id': account_id }),
    )


def get_account_users_data(self, access_token, account_id):
    return self.client.get(
        f'/api/account',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps({ 'id': account_id }),
    )


def create_account_default_allowance(self, access_token):
    return self.client.post(
        f'/api/account',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps({
            'allowance': app.config['MCS_DEFAULT_ACCOUNT_ALLOWANCE'],
        }),
    )


def create_account_custom_allowance(self, access_token, custom_allowance):
    return self.client.post(
        f'/api/account',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps({ 'allowance': custom_allowance })
    )


class TestAccountBlueprint(BaseTestCase):
    def test_account_post(self):
        ''' Test creating a new account '''

        default_allowance = app.config['MCS_DEFAULT_ACCOUNT_ALLOWANCE']

        account_resp = create_account_default_allowance(self, access_token,
                                                        account.id)
        account_data = json.loads(account_resp.data.decode())

        self.assertEqual(account_data['balance'], 0)
        self.assertEqual(account_data['allowance'], default_allowance)


        custom_allowance = 9999
        account_resp = create_account_custom_allowance(self, access_token,
                                                       account.id,
                                                       custom_allowance)
        account_data = json.loads(account_resp.data.decode())

        self.assertEqual(account_data['balance'], 0)
        self.assertEqual(account_data['allowance'], custom_allowance)


    def test_account_get(self):
        ''' Test getting an account from DB '''

        # Create a mock account (w/ default allowance)
        account = Account()

        db.session.add(account)
        db.session.commit()

        account_resp = get_account_data(self, access_token, account.id)
        account_data = json.loads(account_resp.data.decode())

        self.assertEqual(account_data['id'], account.id)
        self.assertEqual(account_data['balance'], accou

        db.session.add(user)
        db.session.commit()nt.balance)
        self.assertEqual(account_data['allowance'], account.allowance)


    def test_account_users_get(self):
        ''' Test getting users associated with account from DB '''

        # Create a mock user
        username_0 = 'alice'
        user_0 = User(username=username_0)

        db.session.add(user_0)
        db.session.commit()

        # Create another mock user
        username_1 = 'bob'
        user_1 = User(username=username_1)

        db.session.add(user_1)
        db.session.commit()

        # Create a mock account (w/ default allowance)
        account = Account()

        db.session.add(account)
        db.session.commit()

        # Associate user 0 with account0 by mock entry in user_account table
        user_account = UserAccount(user_id=user_0.id, account_id=account.id)

        db.session.add(user_account)
        db.session.commit()

        # Associate user 1 with account0 by mock entry in user_account table
        user_account = UserAccount(user_id=user_1.id, account_id=account.id)

        db.session.add(user_account)
        db.session.commit()

        account_users_resp = get_account_users_data(self, access_token,
                                                    account.id)
        account_users_data = json.loads(account_users_resp.data.decode())

        """ Expected
        d = {
            'account': {
                'id': 1,
                'users': [
                    { 'username': username_0 },
                    { 'username': username_1 }
                ]
            }
        }
        """

        self.assertTrue(account_users_resp.status)
        self.assertEqual(account_users_resp.status_code, 200)
        self.assertEqual(account_users_data['account']['id'], account.id)
        self.assertEqual(len(account_users_data['account']['users']), 2)
        users_data = account_users_data['account']['users']
        self.assertEqual(users_data[0]['username'], username_0)
        self.assertEqual(users_data[1]['username'], username_1)
