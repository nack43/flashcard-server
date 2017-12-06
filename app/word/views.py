from . import word

from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify
from app.models import Word, User


@word.route('/word/register', methods=['POST'])
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


@word.route('/word/all', methods=['GET'])
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
                    'front': word.front,
                    'back': word.back
                }
                
                word_list.append(element)

            return make_response(jsonify(word_list)), 200


