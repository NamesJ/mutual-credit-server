from app import db
from app.models.offer import Offer
from app.models.schemas import OfferSchema

from tests.utils.base import BaseTestCase


class TestOfferModel(BaseTestCase):
    def test_schema(self):
        o = Offer(
            seller=1,
            title='Scary Spooky Skeleton',
            price=47,
            description='1x very large, very scary, and very spooky skeleton',
        )
        o_dump = OfferSchema().dump(o)

        self.assertTrue(o_dump['seller'] == 1)
        self.assertTrue(o_dump['title'] == 'Scary Spooky Skeleton')
        self.assertTrue(o_dump['price'] == 47)
        self.assertTrue(o_dump['description'] == '1x very large, very scary, and very spooky skeleton')
