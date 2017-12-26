from flask_api import status
from . import pos_blueprint
from flask import make_response, request, jsonify
from app.models import User, Part_of_speech

@pos_blueprint.route('/v1/poses', methods=['GET'])
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
                    'type': pos.type,
                    'created_at': pos.created_date,
                    'modified_at': pos.modified_date
                }

                pos_list.append(element)
            
            return make_response(jsonify(pos_list)), status.HTTP_200_OK

