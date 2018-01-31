from . import answer_blueprint
from flask_api import status
from flask import Blueprint, make_response, request, jsonify
from app.models import Word, User
from app.decorators import token_auth


@answer_blueprint.route('/v1/answers', methods=['POST'])
@token_auth
def get_answers():
    answers = request.get_json()

    for answer in answers:

        word = Word.query.filter_by(id=answer['word_id']).first()

        if answer['is_correct'] == True:
            word.weight = word.weight - 1

        else:
            word.weight = word.weight + 1

        word.save()

    return '', status.HTTP_200_OK

