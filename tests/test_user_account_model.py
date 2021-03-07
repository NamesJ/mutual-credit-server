from app import db
from app.models.user_account import UserAccount
from app.models.schemas import UserAccountSchema

from tests.utils.base import BaseTestCase


class TestUserAccountModel(BaseTestCase):
    def test_schema(self):
        ua = UserAccount(
            user_id=7,
            account_id=13,
        )
        ua_dump = UserAccountSchema().dump(ua)

        self.assertTrue(a_dump['user_id'] == 7)
        self.assertTrue(a_dump['account_id'] == 13)
