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
            'front': '巴士', 
            'back': 'バス',
            'pos_id': 2 
        }

        self.user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

            # insert test recode for POS
            pos_1 = Part_of_speech(type='None')
            pos_2 = Part_of_speech(type='Noun')
            pos_1.save()
            pos_2.save()

            # insert test recode for Choice
            choice_1 = Choice(choice='ニーチェ', pos_id=2)
            choice_2 = Choice(choice='ハイデガー', pos_id=2)
            choice_3 = Choice(choice='サルトル', pos_id=2)
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

        res_1 = self.word_register(access_token, self.word_data)
        res_2 = self.word_register(access_token, self.word_data_2)

        # convert response to json format
        res_json_1 = json.loads(res_1.data.decode())
        res_json_2 = json.loads(res_2.data.decode())

        # in case of pos_id 1
        self.assertEqual(res_json_1['id'], 1)
        self.assertEqual(res_json_1['front'], '你好')
        self.assertEqual(res_json_1['back'], 'こんにちは')
        self.assertEqual(res_json_1['weight'], 0)
        self.assertIs(type(res_json_1['choices'][0]), str)
        self.assertIs(type(res_json_1['choices'][1]), str)
        self.assertIs(type(res_json_1['choices'][2]), str)
        self.assertIs(type(res_json_1['created_by']), int)
        self.assertEqual(res_json_1['pos_id'], 1)
        self.assertIs(type(res_json_1['created_at']), str)
        self.assertIs(type(res_json_1['modified_at']), str)
        self.assertEqual(res_1.status_code, 201)

        # in case of pos_id except for 1
        self.assertEqual(res_json_2['id'], 2)
        self.assertEqual(res_json_2['front'], '巴士')
        self.assertEqual(res_json_2['back'], 'バス')
        self.assertEqual(res_json_2['weight'], 0)
        self.assertIs(type(res_json_2['choices'][0]), str)
        self.assertIs(type(res_json_2['choices'][1]), str)
        self.assertIs(type(res_json_2['choices'][2]), str)
        self.assertIs(type(res_json_2['created_by']), int)
        self.assertEqual(res_json_2['pos_id'], 2)
        self.assertIs(type(res_json_2['created_at']), str)
        self.assertIs(type(res_json_2['modified_at']), str)
        self.assertEqual(res_2.status_code, 201)


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
        self.assertIn(res_json[1]['front'], '巴士')
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


    def test_word_delete(self):

        self.sign_up()
        access_token = self.login()
        
        self.word_register(access_token, self.word_data)

        res = self.client().delete(
                '/v1/words',
                headers=dict(Authorization="Bearer " + access_token),
                content_type='application/json',
                data=json.dumps(dict(word_id=1))
                )

        self.assertEqual(res.status_code, 204)


    def test_word_delete_does_not_exist(self):

        self.sign_up()
        access_token = self.login()
        
        self.word_register(access_token, self.word_data)

        # word_id 2 does not exist
        res = self.client().delete(
                '/v1/words',
                headers=dict(Authorization="Bearer " + access_token),
                content_type='application/json',
                data=json.dumps(dict(word_id=2))
                )

        self.assertEqual(res.status_code, 404)
    
