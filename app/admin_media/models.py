from app import db
from datetime import datetime


# ADMIN MEDIA models

class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_width = db.Column(db.Integer, nullable=False)
    file_height = db.Column(db.Integer, nullable=False)
    image_type_id = db.Column(db.Integer, db.ForeignKey('image_type.id'), nullable=False)
    post = db.relationship('Post', backref='image1', lazy='dynamic')
    page_home_main = db.relationship('PageHomeMain', backref='image1', lazy='dynamic')
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def getImage(image_id):
        return Images.query.filter_by(id=image_id).first()

    def __repr__(self):
        return '<Images {}>'.format(self.filename)


class ImageType(db.Model):
    __tablename__ = 'image_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    images = db.relationship('Images', backref='image_type', lazy='dynamic')

    def __repr__(self):
        return '<ImageType {}>'.format(self.name)
