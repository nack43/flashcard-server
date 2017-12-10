from . import word

from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify
from app.models import Word, User, Part_of_speech


@word.route('/v1/word/register', methods=['POST'])
def word_register():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            # handle pattern of the authenticated user
            front = request.data.get('front', '')
            back = request.data.get('back', '')
            pos_id = request.data.get('pos_id', '')

            word = Word(
                    front=front,
                    back=back,
                    created_by=user_id,
                    pos_id=pos_id
                )
            
            word.choice_determination(pos_id)
            word.save()

            response = {
                'message': 'Registered Successfully.',
                'front': front,
                'back': back,
                'created_by': user_id,
                'pos_id': pos_id
            }

            return make_response(jsonify(response)), 201


@word.route('/v1/word/all', methods=['GET'])
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

@word.route('/v1/word/pos_all', methods=['GET'])
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


@word.route('/v1/word/test_result', methods=['POST'])
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

