from flask import Blueprint

bp = Blueprint('admin_page', __name__)

from app.admin_page import routes
