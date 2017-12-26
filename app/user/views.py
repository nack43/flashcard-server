from flask_api import status
from . import user_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


class RegistrationView(MethodView):

    def post(self):
        """Handle POST request for this view. Url ---> /v1/users"""
        content = request.get_json()
        email = content['email'] 
        password = content['password']

        user = User.query.filter_by(email=email).first()

        if not user:

            new_user = User(email=email, password=password)
            new_user.save()

            return '', status.HTTP_201_CREATED

        else:

            response = {
                'message': 'User already exists. Please login.'
            }

            return jsonify(response), status.HTTP_409_CONFLICT


# Define the API resource
registration_view = RegistrationView.as_view('register_view')

# Define the rule for the registration url ---> /v1/users
# Then add the rule to the blueprint
user_blueprint.add_url_rule(
    '/v1/users',
    view_func=registration_view,
    methods=['POST']
)


