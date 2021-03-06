from app import db
from app.models.transfer import Transfer
from app.models.schemas import TransferSchema

from tests.utils.base import BaseTestCase

from datetime import datetime


class TestUserModel(BaseTestCase):
    def test_schema(self):
        t = Transfer(
            sender=1,
            receiver=2,
            value=17,
            memo='gas money',
        )
        t_dump = TransferSchema().dump(t)

        self.assertTrue(t_dump['sender'] == 1)
        self.assertTrue(t_dump['receiver'] == 2)
        self.assertTrue(t_dump['value'] == 17)
        self.assertTrue(t_dump['memo'] == 'gas money')
