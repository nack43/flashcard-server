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
    access_token = db.Column(db.String(256), nullable=True)
    words = db.relationship(
        'Word', order_by='Word.id', cascade="all, delete-orphan")

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
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )

            self.access_token = jwt_string

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
        return "<User: {}>".format(self.id)


class Part_of_speech(db.Model):
    __tablename__ = 'part_of_speeches'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    words = db.relationship(
        'Word', order_by='Word.id', cascade="all, delete-orphan")
    choices = db.relationship(
        'Choice', order_by='Choice.id', cascade="all, delete-orphan")


    def save(self):
        db.session.add(self)
        db.session.commit()


class Choice(db.Model):
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(256), nullable=False)
    part_of_speech_id = db.Column(db.Integer, db.ForeignKey(Part_of_speech.id), nullable=False)
    words = db.relationship(
        'Word', order_by='Word.id', cascade="all, delete-orphan")

    def save(self):
        db.session.add(self)
        db.session.commit()


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(256), nullable=False)
    back = db.Column(db.String(256), nullable=False)
    wight = db.Column(db.Integer, nullable=False)
    choice_1 = db.Column(db.Integer, db.ForeignKey(Choice.id), nullable=False)
    choice_2 = db.Column(db.Integer, db.ForeignKey(Choice.id), nullable=False)
    choice_3 = db.Column(db.Integer, db.ForeignKey(Choice.id), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    part_of_speech_id = db.Column(db.Integer, db.ForeignKey(Part_of_speech.id), nullable=False)

    def __init__(self, front, back, created_by, part_of_speech_id):
        self.front = front
        self.back = back
        self.wight = 0
        self.created_by = created_by
        self.part_of_speech_id = part_of_speech_id


    def save(self):
        db.session.add(self)
        db.session.commit()

