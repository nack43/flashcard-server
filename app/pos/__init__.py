from flask import Blueprint

pos_blueprint = Blueprint('pos', __name__)

from . import views

