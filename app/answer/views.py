from . import answer_blueprint
from flask_api import status
from flask import Blueprint, make_response, request, jsonify
from app.models import Word, User


@answer_blueprint.route('/v1/answers', methods=['POST'])
def get_answers():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            answers = request.get_json()

            for answer in answers:
                if answer['is_correct'] == False:
                    word = Word.query.filter_by(id=answer['word_id']).first()
                    word.weight = word.weight + 1
                    word.save()

            return '', status.HTTP_200_OK

