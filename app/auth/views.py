from flask_api import status
from .import auth_blueprint
from flask import make_response, request, jsonify
from app.models import User

@auth_blueprint.route('/v1/authentication', methods=['POST'])
def login():

    content = request.get_json()
    email = content['email']
    password = content['password']

    user = User.query.filter_by(email=email).first()

    if user and user.password_is_valid(password):
        user.generate_token(user.id)

        if user.access_token:
            response = {
                'access_token': user.access_token.decode()
            }

            return make_response(jsonify(response)), status.HTTP_200_OK
    else:

        response = {
            'message': 'Invalid email or password.'
            }

        return make_response(jsonify(response)), status.HTTP_401_UNAUTHORIZED






