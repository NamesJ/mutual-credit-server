from app import db
from app.models.account import Account
from app.models.schemas import AccountSchema

from tests.utils.base import BaseTestCase


class TestAccountModel(BaseTestCase):
    def test_schema(self):
        a = Account(
            balance=0,
            allowance=100,
        )
        a_dump = AccountSchema().dump(a)

        self.assertTrue(a_dump['balance'] == 0)
        self.assertTrue(a_dump['allowance'] == 100)
