from flask import Blueprint


wapi = Blueprint('wapi', __name__)
from . import views, auth
