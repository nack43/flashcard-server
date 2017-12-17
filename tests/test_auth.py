import unittest
import json

from app import create_app, db

class AuthTestCase(unittest.TestCase):
    """Test case for the auth blueprint"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        
        self.user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }
        
        self.not_a_user = {
            'email': 'not_a_user@test.com',
            'password': 'nope'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()


    def test_login(self):
        """Test registered user can login."""
        res_1 = self.client().post(
                '/v1/users',
                content_type='application/json',
                data=json.dumps(self.user_data)
                )

        res_2 = self.client().post(
                '/v1/authentication',
                content_type='application/json',
                data=json.dumps(self.user_data)
                )

        result = json.loads(res_2.data.decode())

        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(['access_token'])


    def test_non_registered_user_login(self):
        """Test non registered users cannot login."""
        res_1 = self.client().post(
                '/v1/users',
                content_type='application/json',
                data=json.dumps(self.not_a_user)
                )
        
        res_2 = self.client().post(
                '/v1/authentication',
                content_type='application/json',
                data=json.dumps(self.not_a_user)
                )

        result = json.loads(res_2.data.decode())

        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Invalid email or password.")

