#standard library
import unittest
import json

from app import create_app, db

class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.word_data = {
            'front': '你好',
            'back': 'こんにちは' 
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()


    def test_word_registration(self):
        """Testing for word registration normally."""
        res = self.client().post(
                '/word/register', 
                data=self.word_data,
                headers=dict(Authorization="Bearer " + access_token)
                )

        # convert response to json format
        res_json = json.loads(res.data.decode())

        self.assertEqual(res_json['message'], 'Registered Successfully.')
        self.assertEqual(res_json['front'], '你好')
        self.assertEqual(res_json['back'], 'こんにちは')
        self.assertEqual(res.status_code, 201)


