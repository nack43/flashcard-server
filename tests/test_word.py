import unittest
import json
from datetime import datetime

from app import create_app, db
from app.models import Part_of_speech, Choice

class WordTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client
        self.word_data = {
            'front': '你好',
            'back': 'こんにちは',
            'pos_id': 1
        }
        
        self.word_data_2 = {
            'front': '早晨', 
            'back': 'おはよう',
            'pos_id': 1
        }
        self.word_data_3 = {
            'front': '多謝',
            'back': 'ありがとう',
            'pos_id': 1
        }

        self.word_data_4 = {
            'front': '早抖',
            'back': 'おやすみ',
            'pos_id': 1
        }
        self.word_data_5 = {
            'front': '日文',
            'back': '日本語',
            'pos_id': 1
        }

        self.user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }

        self.test_result = {
                1: {
                    'word_id': 1, 
                    'is_correct': True
                    },
                2: {
                    'word_id': 2,
                    'is_correct': True
                    },
                3: {
                    'word_id': 3,
                    'is_correct': False
                    },
                4: {
                    'word_id': 4,
                    'is_correct': False
                    },
                5: {
                    'word_id': 5,
                    'is_correct': False
                    }
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

            # insert test recode for Choice
            choice_1 = Choice(choice='ニーチェ', pos_id=1)
            choice_2 = Choice(choice='ハイデガー', pos_id=1)
            choice_3 = Choice(choice='サルトル', pos_id=1)
            choice_1.save()
            choice_2.save()
            choice_3.save()
            

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

    def word_register(self, access_token, word):

        res = self.client().post(
                '/v1/words', 
                headers=dict(Authorization="Bearer " + access_token),
                content_type='application/json',
                data=json.dumps(word)
                )

        return res

    def test_word_registration(self):
        """Testing for word registration normally."""
        self.sign_up()
        access_token = self.login()

        res = self.word_register(access_token, self.word_data)

        # convert response to json format
        res_json = json.loads(res.data.decode())

        self.assertEqual(res_json['id'], 1)
        self.assertEqual(res_json['front'], '你好')
        self.assertEqual(res_json['back'], 'こんにちは')
        self.assertEqual(res_json['weight'], 0)
        self.assertIs(type(res_json['choices'][0]), str)
        self.assertIs(type(res_json['choices'][1]), str)
        self.assertIs(type(res_json['choices'][2]), str)
        self.assertIs(type(res_json['created_by']), int)
        self.assertEqual(res_json['pos_id'], 1)
        self.assertIs(type(res_json['created_at']), str)
        self.assertIs(type(res_json['modified_at']), str)
        self.assertEqual(res.status_code, 201)


    def test_get_all_words(self):
        """Testing for getting all words user have"""
        self.sign_up()
        access_token = self.login()

        self.word_register(access_token, self.word_data)
        self.word_register(access_token, self.word_data_2)

        res = self.client().get(
                '/v1/words',
                headers=dict(Authorization="Bearer " + access_token)
                )
        
        res_json = json.loads(res.data.decode())

        self.assertIn(res_json[0]['front'], '你好')
        self.assertIn(res_json[1]['front'], '早晨')
        self.assertEqual(res.status_code, 200)

    def test_get_all_words_after_requested_modified_date(self):
        """Testing for getting all words after requested modified date"""
        self.sign_up()
        access_token = self.login()

        self.word_register(access_token, self.word_data)

        now = datetime.utcnow().isoformat()

        self.word_register(access_token, self.word_data_2)

        res = self.client().get(
                '/v1/words',
                headers=dict(Authorization="Bearer " + access_token),
                query_string=dict(modified_at=now)
                )
        
        res_json = json.loads(res.data.decode())

        self.assertIs(len(res_json), 1)
        self.assertEqual(res.status_code, 200)
    
    def test_receive_test_result(self):
        """Tesgin for receiving test result."""

        self.sign_up()
        access_token = self.login()
        
        res_1 = self.client().post(
                '/v1/words', 
                data=self.word_data,
                headers=dict(Authorization="Bearer " + access_token)
                )
        res_2 = self.client().post(
                '/v1/words', 
                data=self.word_data_2,
                headers=dict(Authorization="Bearer " + access_token)
                )
        res_3 = self.client().post(
                '/v1/words', 
                data=self.word_data_3,
                headers=dict(Authorization="Bearer " + access_token)
                )
        res_4 = self.client().post(
                '/v1/words', 
                data=self.word_data_4,
                headers=dict(Authorization="Bearer " + access_token)
                )
        res_5 = self.client().post(
                '/v1/words', 
                data=self.word_data_5,
                headers=dict(Authorization="Bearer " + access_token)
                )


        res_6 = self.client().post(
            '/v1/tests',
            data=json.dumps(dict(self.test_result)),
            content_type='application/json',
            headers=dict(Authorization="Bearer " + access_token)
            )

        self.assertEqual(res_6.status_code, 200)


