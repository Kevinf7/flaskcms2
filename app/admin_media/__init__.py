from flask import Blueprint

bp = Blueprint('admin_media', __name__)

from app.admin_media import routes
