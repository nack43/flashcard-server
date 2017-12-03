#standard library
import unittest
import json

from app import create_app, db
from app.models import Part_of_speech
class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.word_data = {
            'front': '你好',
            'back': 'こんにちは',
            'part_of_speech_id': 1
        }

        self.user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

            # insert test recode
            pos = Part_of_speech(type='noun')
            pos.save()

    def sign_up(self):
        return self.client().post('/auth/register', data=self.user_data)


    def login(self):
        return self.client().post('/auth/login', data=self.user_data)


    def test_word_registration(self):
        """Testing for word registration normally."""
        self.sign_up()
        login_res = self.login()
        access_token = json.loads(login_res.data.decode())['access_token']

        res = self.client().post(
                '/word/register', 
                data=self.word_data,
                headers=dict(Authorization="Bearer " + access_token)
                )

        # convert response to json format
        res_json = json.loads(res.data.decode())
        print(res_json)

        self.assertEqual(res_json['message'], 'Registered Successfully.')
        self.assertEqual(res_json['front'], '你好')
        self.assertEqual(res_json['back'], 'こんにちは')
        self.assertEqual(res.status_code, 201)


