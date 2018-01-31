from flask_api import status
from . import pos_blueprint
from flask import make_response, request, jsonify
from app.models import User, Part_of_speech
from app.decorators import token_auth

@pos_blueprint.route('/v1/poses', methods=['GET'])
@token_auth
def get_all_pos():
    
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

