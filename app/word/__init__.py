from flask import Blueprint

word = Blueprint('word', __name__)

from . import views

