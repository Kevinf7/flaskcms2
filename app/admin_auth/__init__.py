from flask import Blueprint

bp = Blueprint('admin_auth', __name__)

from app.admin_auth import routes
