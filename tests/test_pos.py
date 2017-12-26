import unittest
import json

from app import create_app, db
from app.models import Part_of_speech

class PosTestCase(unittest.TestCase):

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
            
            # insert test recode for POS
            pos_1 = Part_of_speech(type='noun')
            pos_2 = Part_of_speech(type='verb')
            pos_1.save()
            pos_2.save()

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

    def test_get_all_pos(self):
        """Testing for getting all pos (part of spheeches)"""
        self.sign_up()
        access_token = self.login()

        res = self.client().get(
            '/v1/poses',
            headers=dict(Authorization="Bearer " + access_token)
            )

        res_json = json.loads(res.data.decode())

        self.assertEqual(res_json[0]['id'], 1)
        self.assertEqual(res_json[0]['type'], 'noun')
        self.assertIs(type(res_json[0]['created_at']), str)
        self.assertIs(type(res_json[0]['modified_at']), str)
        self.assertEqual(res_json[1]['id'], 2)
        self.assertEqual(res_json[1]['type'], 'verb')
        self.assertIs(type(res_json[1]['created_at']), str)
        self.assertIs(type(res_json[1]['modified_at']), str)
        self.assertEqual(res.status_code, 200)


