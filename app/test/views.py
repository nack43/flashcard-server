from . import test_blueprint
from flask_api import status
from flask import Blueprint, make_response, request, jsonify
from app.models import Word, User


@test_blueprint.route('/v1/tests', methods=['POST'])
def get_test_result():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            test_results = request.get_json()
            print(test_results)

            for result in test_results:
                if result['is_correct'] == False:
                    word = Word.query.filter_by(id=result['word_id']).first()
                    word.weight = word.weight + 1
                    word.save()

            return '', status.HTTP_200_OK

