from flask import Blueprint

answer_blueprint = Blueprint('answer', __name__)

from . import views

