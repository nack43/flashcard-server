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
        res = self.client().post('/word/register', data=self.word_data)
        result = json.loads(res.data.decode())

        self.assertEqual(result['message'], 'Registered Successfully.')
        self.assertEqual(res.status_code, 201)


    def test_get_all_words(self):
        # word registration
        res = self.client().post('/word/register', data=self.word_data)
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        # get all words 
        res_get = self.client().get('/word', headers=dict(Authorization="Bearer " + access_token))
        result_get = json.loads(res.data.decode())

        self.assertEqual(res_get.status_code, 200)
        self.assertIn('你好', str(res_get.data))

