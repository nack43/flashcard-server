# standard library
import unittest
import json

# local import
from app import create_app, db


class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # initialize the test client
        self.client = self.app.test_client
        # test password and email definition
        self.user_data = {
            'email': 'test@test.com',
            'password': 'test_password'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()


    def test_registration(self):
        """Test user registration works correctly."""
        res = self.client().post('/v1/auth/register', data=self.user_data)
        # convert api resonse to json format
        result = json.loads(res.data.decode())

        self.assertEqual(result['message'], "Registered successfully.")
        self.assertEqual(res.status_code, 201)


    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client().post('/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/v1/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)

        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists. Please login.")


    def test_login(self):
        """Test registered user can login."""
        res = self.client().post('/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/v1/auth/login', data=self.user_data)

        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(['access_token'])


    def test_non_registered_user_login(self):
        """Test non registered users cannot login"""
        # define a dictionary to represent an unregistered user
        not_a_user = {
            'email': 'not_a_user@test.com',
            'password': 'nope'
        }

        res = self.client().post('/v1/auth/login', data=not_a_user)
        result = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again.")


        def tearDown(self):
            """teardown all initialized variables."""
            with self.app.app_context():
                db.session.remove()
                db.drop_all()


if __name__ == "__main__":
    unittest.run()
