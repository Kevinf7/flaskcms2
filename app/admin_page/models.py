from app import db
from datetime import datetime


# ADMIN PAGE models

class Page(db.Model):
    __tablename__ = 'page'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    display = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_publish_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    page_home_main = db.relationship(
        "PageHomeMain", backref="page", lazy="dynamic")

    @staticmethod
    def getPage(name):
        return Page.query.filter_by(name=name).first()

    def __repr__(self):
        return '<Page {}>'.format(self.name)


class PageStatus(db.Model):
    __tablename__ = 'page_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    page_home_main = db.relationship(
        "PageHomeMain", backref="page_status", lazy="dynamic")

    @staticmethod
    def getStatus(name):
        return PageStatus.query.filter_by(name=name).first()

    def __repr__(self):
        return '<PageStatus {}>'.format(self.name)


class PageHomeMain(db.Model):
    __tablename__ = 'page_home_main'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    image_id1 = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('page_status.id'), nullable=False)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    update_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<PageHomeMain {}>'.format(self.heading)

