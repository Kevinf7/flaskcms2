from flask import Blueprint

bp = Blueprint('admin_blog', __name__)

from app.admin_blog import routes_blog, routes_tag, routes_comment
