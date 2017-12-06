# standard library
import random
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
    words = db.relationship('Word')

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
    words = db.relationship('Word')
    choices = db.relationship('Choice')


    def save(self):
        db.session.add(self)
        db.session.commit()


class Choice(db.Model):
    __tablename__ = 'choices'
    id = db.Column(db.Integer, primary_key=True)
    choice = db.Column(db.String(256), nullable=False)
    pos_id = db.Column(db.Integer, db.ForeignKey(Part_of_speech.id), nullable=False)
#    words = db.relationship('Word')

    # for testing
    def __init__(self, choice, pos_id):
        self.choice = choice
        self.pos_id = pos_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(256), nullable=False)
    back = db.Column(db.String(256), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    choice_1_id = db.Column(db.Integer, db.ForeignKey(Choice.id), nullable=False)
    choice_2_id = db.Column(db.Integer, db.ForeignKey(Choice.id), nullable=False)
    choice_3_id = db.Column(db.Integer, db.ForeignKey(Choice.id), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    pos_id = db.Column(db.Integer, db.ForeignKey(Part_of_speech.id), nullable=False)

    choice_1 = db.relationship('Choice', foreign_keys=[choice_1_id])
    choice_2 = db.relationship('Choice', foreign_keys=[choice_2_id])
    choice_3 = db.relationship('Choice', foreign_keys=[choice_3_id])

    def __init__(self, front, back, created_by, pos_id):
        self.front = front
        self.back = back
        self.wight = 0
        self.created_by = created_by
        self.pos_id = pos_id

    def choice_determination(self, pos_id):
        choice_list = Choice.query.filter_by(pos_id=pos_id).all()
        random.shuffle(choice_list)
        self.choice_1_id = choice_list[0].id
        self.choice_2_id = choice_list[1].id
        self.choice_3_id = choice_list[2].id

    @staticmethod
    def get_all(user_id):
        return Word.query.filter_by(created_by=user_id).all()


    def save(self):
        db.session.add(self)
        db.session.commit()

