from flask import Blueprint

bp = Blueprint('admin_shop', __name__)

from app.admin_shop import routes
