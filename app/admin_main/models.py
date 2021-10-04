from app import db
from datetime import datetime


# ADMIN MAIN models

class SiteSetting(db.Model):
    __tablename__ = 'site_setting'

    id = db.Column(db.Integer, primary_key=True)
    posts_per_page = db.Column(db.Integer)
    google_map_key = db.Column(db.String(100))
    recaptcha_key = db.Column(db.String(100))
    sendgrid_key = db.Column(db.String(100))
    mail_from = db.Column(db.String(50))
    mail_admins = db.Column(db.String(500))
    comment_banned = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    update_date = db.Column(db.DateTime,default=datetime.utcnow)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<SiteSettings {}>'.format(self.id)


