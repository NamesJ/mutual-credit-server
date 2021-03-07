import json

from flask_jwt_extended import create_access_token

from app import db
from app.models.account import Account
from app.models.user import User
from app.models.user_account import UserAccount

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user


def get_user_data(self, access_token, username):
    return self.client.get(
        f"/api/user/{username}",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )


def get_user_accounts_data(self, access_token, username):
    return self.client.get(
        f"/api/user/accounts",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
        data=json.dumps({ 'username': username }),
    )


class TestUserBlueprint(BaseTestCase):
    def test_user_get(self):
        """ Test getting a user from DB """

        # Create a mock user
        username = "test1234"
        user = User(username=username)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        user_resp = get_user_data(self, access_token, username)
        user_data = json.loads(user_resp.data.decode())

        self.assertTrue(user_resp.status)
        self.assertEqual(user_resp.status_code, 200)
        self.assertEqual(user_data["user"]["username"], username)

        # Test a 404 request
        user_404_resp = get_user_data(self, access_token, "non.existent")
        self.assertEqual(user_404_resp.status_code, 404)


    def test_user_accounts_get(self):
        ''' Test getting accounts for a user from DB '''

        # Create a mock user
        username = 'alice'
        user = User(username=username)

        db.session.add(user)
        db.session.commit()

        # Create a mock account
        account = Account(allowance=100)

        db.session.add(account)
        db.session.commit()

        # Create a mock user-account association
        user_account = UserAccount(user_id=user.id, account_id=account.id)

        db.session.add(user_account)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        user_accounts_resp = get_user_accounts_data(self, access_token, username)
        user_accounts_data = json.loads(user_accounts_resp.data.decode())

        self.assertTrue(user_accounts_resp.status)
        self.assertEqual(user_accounts_resp.status_code, 200)
        self.assertEqual(user_accounts_data['user']['username'], username)
        self.assertEqual(len(user_accounts_data['user']['accounts']), 1)
        accounts_data = user_accounts_data['user']['accounts']
        self.assertEqual(account_data[0]['id'], account.id)
        self.assertEqual(account_data[0]['balance'], account.balance)
        self.assertEqual(account_data[0]['allowance'], account.allowance)
