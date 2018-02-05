from . import word
from datetime import datetime 
from flask.views import MethodView
from flask_api import status
from flask import Blueprint, make_response, request, jsonify
from app.models import Word, User, Part_of_speech, Choice
from sqlalchemy import and_
from app.decorators import token_auth


class WordAPI(MethodView):

    # get user id from access token
    def get_user_id(self):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]
        user_id = User.decode_token(access_token)

        return user_id


    def get(self):
   
        # get a user_id from access_token
        user_id = self.get_user_id() 

        requested_modified_at = request.args.get('modified_at')

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


    def post(self):
        # get a user_id from access_token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]
        user_id = User.decode_token(access_token)

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


    def delete(self, id):

        word = Word.query.filter_by(id=id).first()

        if word:
            word.delete()
            
            return '', status.HTTP_204_NO_CONTENT

        else:

            return '', status.HTTP_404_NOT_FOUND


# Add decorator to each function in WordAPI class
word_view = token_auth(WordAPI.as_view('word_api'))

# Add url to the blueprint
word.add_url_rule('/v1/words', view_func=word_view, methods=['GET', 'POST'])
word.add_url_rule('/v1/words/<int:id>', view_func=word_view, methods=['DELETE'])


