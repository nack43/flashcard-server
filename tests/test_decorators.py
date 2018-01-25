import unittest
import json
from app import create_app, db
from app.models import Part_of_speech


class DecoratorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        self.user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

            pos_1 = Part_of_speech(type='None')
            pos_1.save()


    def sign_up(self):
        return self.client().post(
                '/v1/users',
                content_type='application/json',
                data=json.dumps(self.user_data)
                )

    def login(self):

        res = self.client().post(
                '/v1/authentication',
                content_type='application/json',
                data=json.dumps(self.user_data)
                )

        access_token = json.loads(res.data.decode())['access_token']

        return access_token

    def test_invalid_token(self):

        invalid_token = 'invalid token'

        res = self.client().get(
            '/v1/poses',
            headers=dict(Authorization="Bearer " + invalid_token)
            )

        res_json = json.loads(res.data.decode())

        self.assertEqual(res_json['message'], 'Invalid token')
        self.assertEqual(res.status_code, 401)

    def test_no_auth_header(self):

        res = self.client().get(
            '/v1/poses'
            )

        self.assertEqual(res_json['message'], 'No Authorization header')
        self.assertEqual(res.status_code, 401)
            

