from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime, timedelta
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login_manager


# ADMIN AUTH models

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(200))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    prev_login = db.Column(db.DateTime,default=datetime.utcnow, nullable=True)
    last_login = db.Column(db.DateTime,default=datetime.utcnow, nullable=True)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    pages = db.relationship('Page', backref='last_publish_by', lazy='dynamic')
    page_home_main = db.relationship('PageHomeMain', backref='author', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    site_setting = db.relationship('SiteSetting', backref='user', lazy='dynamic')

    # generate hash of given password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # return hash of given password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=monsterid&s={}'.format(digest, size)

    # return true if user is admin, false otherwise
    def is_admin(self):
        return self.role.name == 'admin'

    # creates token of user object
    # decode('utf-8') converts token to string
    def get_reset_password_token(self, expires_in=current_app.config['FORGOT_PASSWORD_TOKEN_EXPIRE']):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    # decodes token and returns user object
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def to_dict(self):
        data = {
            'email' : self.email,
            'first_name' : self.firstname,
            'last_name' : self.lastname
        }
        return data

    def __repr__(self):
        return '<User {}>'.format(self.email)


# This allows application to freely call these methods even if you're not logged in
class AnonymousUser(AnonymousUserMixin):
    def set_password(self, password):
        return False
    def check_password(self, password):
        return False
    def avatar(self, size):
        return False
    def is_admin(self):
        return False
    def get_reset_password_token(self, expires_in=current_app.config['FORGOT_PASSWORD_TOKEN_EXPIRE']):
        return False
# This tells flask login which class to use if user is not logged in
login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    __tablename__='role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User',backref='role',lazy='dynamic')


# Used by flask-login
# This callback is used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)