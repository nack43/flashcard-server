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
            part_of_speech_id = request.data.get('part_of_speech_id', '')

            word = Word(
                    front=front,
                    back=back,
                    created_by=user_id,
                    part_of_speech_id=part_of_speech_id
                )

            word.save()

            response = {
                'message': 'Registered Successfully.',
                'front': front,
                'back': back,
                'created_by': user_id,
                'part_of_speech_id': part_of_speech_id
            }

            return make_response(jsonify(response)), 201


