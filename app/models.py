# standard library
from datetime import datetime, timedelta
# third party library
import jwt
from flask_bcrypt import Bcrypt
from flask import current_app
# local import
from app import db


class User(db.Model):
    """Maps to usrs table"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()


    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)


    def save(self):
        db.session.add(self)
        db.session.commit()


    def generate_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            print(jwt_string)

            return jwt_string

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']

        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"

        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


    def __repr__(self):
        return "<User: {}>".format(self.name)


