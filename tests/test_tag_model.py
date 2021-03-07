from app import db
from app.models.tag import Tag
from app.models.schemas import TagSchema

from tests.utils.base import BaseTestCase


class TestTagModel(BaseTestCase):
    def test_schema(self):
        t = Tag(
            entity_type='User.username',
            entity_value='alice',
            tag='spooks',
        )
        t_dump = TagSchema().dump(t)

        self.assertTrue(t_dump['entity_type'] == 'User.username')
        self.assertTrue(t_dump['entity_value'] == 'alice')
        self.assertTrue(t_dump['tag'] == 'spooks')
