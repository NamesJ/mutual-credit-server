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


def create_account_default_allowance(self, access_token):
    return self.client.post(
        f'/api/account',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps({
            'allowance': app.config['MCS_DEFAULT_ACCOUNT_ALLOWANCE'],
        }),
    )


def create_account_custom_allowance(self, access_token, allowance):
    return self.client.post(
        f'/api/account',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json',
        data=json.dumps({ 'allowance': allowance })
    )
