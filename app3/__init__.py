from flask import Blueprint

app3 = Blueprint('app3', __name__, template_folder='templates')

from app3 import app3_routes 
