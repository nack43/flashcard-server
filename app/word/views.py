from . import word
from datetime import datetime 
from flask.views import MethodView
from flask_api import status
from flask import Blueprint, make_response, request, jsonify
from app.models import Word, User, Part_of_speech, Choice
from sqlalchemy import and_


@word.route('/v1/words', methods=['POST'])
def word_register():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):

            content = request.get_json()
            front = content['front']
            back = content['back']
            pos_id = content['pos_id']

            word = Word(
                    front=front,
                    back=back,
                    created_by=user_id,
                    pos_id=pos_id
                )
            
            word.choice_determination(pos_id)
            word.save()
            
            choices = Word.get_word_choices(word) 

            response = {
                'id': word.id,
                'front': word.front,
                'back': word.back,
                'weight': word.weight,
                'choices': choices,
                'created_by': word.created_by,
                'pos_id': word.pos_id,
                'created_at': word.created_date.isoformat(),
                'modified_at': word.modified_date.isoformat()
            }

            return make_response(jsonify(response)), status.HTTP_201_CREATED


@word.route('/v1/words', methods=['GET'])
def get_all_words():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(' ')[1]
    requested_modified_at = request.args.get('modified_at')

    if access_token:
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):

            # get all of words
            if requested_modified_at is None:
                words = Word.get_all(user_id)

            # get all of words after modified_at
            else:
                words = Word.query.filter(and_(Word.created_by == user_id, Word.modified_date > requested_modified_at))

            word_list = []
    
            for word in words:

                choices = Word.get_word_choices(word) 
    
                element = {
                   'id': word.id,
                   'front': word.front,
                   'back': word.back,
                   'weight': word.weight,
                   'choices': choices,
                   'created_by': word.created_by,
                   'pos_id': word.pos_id,
                   'created_at': word.created_date.isoformat(),
                   'modified_at': word.modified_date.isoformat()
                }
                   
                word_list.append(element)
  
            return make_response(jsonify(word_list)), status.HTTP_200_OK

