from .models import User
from flask_api import status
from flask import make_response, request, jsonify

def token_auth(func):
    
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            
            response = {
                    'message': 'No Authorization header'
                }

            return jsonify(response), status.HTTP_401_UNAUTHORIZED

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]

        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):

                return func(*args, **kwargs)
            else:
                response = {
                        'message': 'Invalid token'
                    }

                return jsonify(response), status.HTTP_401_UNAUTHORIZED

    return wrapper


