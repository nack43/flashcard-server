from . import word_blueprint

from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify
from app.models import Word


class RegistrationView(MethodView):

    def post(self):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]
        # access_token validation 
        if access_token:
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # handle pattern of the authenticated user
                front = request.data.get('front', '')
                back = request.data.get('back', '')

                word = Word(front=front, back=back)
                word.save()

                return 201

registration_view = RegistrationView.as_view('register_view')

word_blueprint.add_url_rule(
    '/word/register',
    view_func=registration_view,
    methods=['POST']
}

