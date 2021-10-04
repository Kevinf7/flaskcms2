from flask import Blueprint

bp = Blueprint('admin_main', __name__)

from app.admin_main import routes