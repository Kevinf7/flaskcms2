from flask import current_app
from app import db
from app.admin_main.models import SiteSetting

def set_settings():
    setting=db.session.query(SiteSetting).first()
    current_app.config['SENDGRID_KEY'] = setting.sendgrid_key
    current_app.config['MAIL_FROM'] = setting.mail_from
    if setting.mail_admins:
        current_app.config['MAIL_ADMINS'] = setting.mail_admins.split(' ')
    else:
        current_app.config['MAIL_ADMINS'] = ''
    current_app.config['USER_POSTS_PER_PAGE'] = setting.posts_per_page
    current_app.config['GOOGLE_MAP_KEY'] = setting.google_map_key
    current_app.config['RECAPTCHA_KEY'] = setting.recaptcha_key
    current_app.config['COMMENT_BANNED'] = setting.comment_banned
