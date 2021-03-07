import json

from flask_jwt_extended import create_access_token

from app import db
from app.models.user import User

from tests.utils.base import BaseTestCase
from tests.utils.common import register_user, login_user


def get_user_data(self, access_token, username):
    return self.client.get(
        f"/api/user",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
        data=json.dumps({ 'username': username })
    )


class TestUserBlueprint(BaseTestCase):
    def test_user_get(self):
        """ Test getting a user from DB """

        # Create a mock user
        username = "alice"
        user = User(username=username)

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        user_resp = get_user_data(self, access_token, username)
        user_data = json.loads(user_resp.data.decode())

        self.assertTrue(user_resp.status)
        self.assertEqual(user_resp.status_code, 200)
        self.assertEqual(user_data["user"]["username"], username)
        self.assertTrue(user_data['user']['allowance'] > 0)
        self.assertEqual(user_data['user']['balance'], 0)

        # Test a 404 request
        user_404_resp = get_user_data(self, access_token, "non.existent")
        self.assertEqual(user_404_resp.status_code, 404)
