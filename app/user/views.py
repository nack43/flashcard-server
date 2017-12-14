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

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/users/login"""
        try:
            user = User.query.filter_by(email=request.data['email']).first()

            if user and user.password_is_valid(request.data['password']):
                user.generate_token(user.id)
                if user.access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': user.access_token.decode()
                    }
                    user.save()
                    return make_response(jsonify(response)), 200
            else:

                response = {
                    'message': 'Invalid email or password, Please try again.'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:

            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


# Define the API resource
registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

# Define the rule for the registration url ---> /v1/users
# Then add the rule to the blueprint
user_blueprint.add_url_rule(
    '/v1/users',
    view_func=registration_view,
    methods=['POST']
)

# Define the rule for the registration url ---> /v1/users/login
# Then add the rule to the blueprint
user_blueprint.add_url_rule(
    '/v1/users/login',
    view_func=login_view,
    methods=['POST']
)


