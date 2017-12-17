# standard library
import unittest
import json

# local import
from app import create_app, db


class UserTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # test password and email definition
        self.user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()


    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def test_registration(self):
        """Test user registration works correctly."""
        res = self.client().post(
                '/v1/users',
                content_type='application/json',
                data=json.dumps(self.user_data)
                )

        self.assertEqual(res.status_code, 201)


    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res_1 = self.client().post(
                '/v1/users',
                content_type='application/json',
                data=json.dumps(self.user_data)
                )
        res_2 = self.client().post(
                '/v1/users',
                content_type='application/json',
                data=json.dumps(self.user_data)
                )

        result = json.loads(res_2.data.decode())

        self.assertEqual(result['message'], "User already exists. Please login.")
        self.assertEqual(res_2.status_code, 409)


if __name__ == "__main__":
    unittest.run()

