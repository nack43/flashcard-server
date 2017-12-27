import unittest
import json

from app import create_app, db
from app.models import User, Choice, Part_of_speech


class AnswerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

        self.user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }

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

        self.answers = [
                {
                    'word_id': 1,
                    'is_correct': False
                },
                {
                    'word_id': 2,
                    'is_correct': True
                }
            ]

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

    def test_receive_test_result(self):
        """Tesgin for receiving test result."""

        self.sign_up()
        access_token = self.login()
        
        self.word_register(access_token, self.word_data)
        self.word_register(access_token, self.word_data_2)

        res = self.client().post(
            '/v1/answers',
            data=json.dumps(self.answers),
            content_type='application/json',
            headers=dict(Authorization="Bearer " + access_token)
            )

        self.assertEqual(res.status_code, 200)

