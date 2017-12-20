from . import word

from flask.views import MethodView
from flask_api import status
from flask import Blueprint, make_response, request, jsonify
from app.models import Word, User, Part_of_speech, Choice


@word.route('/v1/words', methods=['POST'])
def word_register():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):

            content = request.get_json()
            front = content['front']
            back = content['back']
            pos_id = content['pos_id']

            word = Word(
                    front=front,
                    back=back,
                    created_by=user_id,
                    pos_id=pos_id
                )
            
            word.choice_determination(pos_id)
            word.save()
            
            choice_1 = Choice.query.filter_by(id=word.choice_1_id).first()
            choice_2 = Choice.query.filter_by(id=word.choice_2_id).first()
            choice_3 = Choice.query.filter_by(id=word.choice_3_id).first()

            choices = [choice_1.choice, choice_2.choice, choice_3.choice]

            response = {
                'id': word.id,
                'front': word.front,
                'back': word.back,
                'weight': word.weight,
                'choices': choices,
                'created_by': word.created_by,
                'pos_id': word.pos_id,
                'created_at': word.created_date,
                'modified_at': word.modified_date
            }

            return make_response(jsonify(response)), status.HTTP_201_CREATED


@word.route('/v1/words', methods=['GET'])
def get_all_words():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            words = Word.get_all(user_id)
            word_list = []

            for word in words:
                element = {
                    'id': word.id,
                    'front': word.front,
                    'back': word.back,
                    'weight': word.weight,
                    'choice_1_id': word.choice_1_id,
                    'choice_2_id': word.choice_2_id,
                    'choice_3_id': word.choice_3_id,
                    'created_by': word.created_by,
                    'pos_id': word.pos_id
                }
                
                word_list.append(element)

            return make_response(jsonify(word_list)), 200

@word.route('/v1/poses', methods=['GET'])
def get_all_pos():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            poses = Part_of_speech.get_all_pos()
            pos_list = []

            for pos in poses:
                element = {
                    'id': pos.id,
                    'type': pos.type
                }

                pos_list.append(element)
            
            return make_response(jsonify(pos_list)), 200


@word.route('/v1/tests', methods=['POST'])
def get_test_result():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            request_json = request.get_json()
            for answer in request_json.values():
                if answer['is_correct'] == False:
                    word = Word.query.filter_by(id=answer['word_id']).first()
                    word.weight = word.weight + 1
                    word.save()

            return 'Successfully'

