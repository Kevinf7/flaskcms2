from app import db
from datetime import datetime
from bs4 import BeautifulSoup


# ADMIN BLOG models

class Tagged(db.Model):
    __tablename__ = 'tagged'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'),primary_key=True)


class Post(db.Model):
    __tablename__='post'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), nullable=False)
    image_id1 = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=True)
    title = db.Column(db.String(100), nullable=False)
    post = db.Column(db.String(15000), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    #joined means all rows returned
    #dynamic means return query objects instead of items so you can use filter
    #cascade delete-orphan means if student object is deleted then association table row is also deleted
    tags = db.relationship('Tagged',foreign_keys=[Tagged.post_id],
                                    backref=db.backref('posts',lazy='joined'),
                                    lazy='joined',
                                    cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def getPost(id):
        return Post.query.filter(Post.id==id).first()

    def getPostBySlug(slug):
        return Post.query.filter(Post.slug==slug).first()

    #return a list of tag names for this post
    def getTagNames(self):
        tags = Tag.query.filter(Tag.posts.any(post_id=self.id)).all()
        return [tag.name for tag in tags]

    #return a string of tag names for this post
    def getTagNamesStr(self):
        return ','.join(self.getTagNames())


    # helper function for search
    def is_txtinHTML(self, str_compare):
        soup = BeautifulSoup(self.post).get_text()
        if soup.lower().count(str_compare.lower()) > 0:
            return True
        else:
            return False

    # return summary of post for search, text only 100 characters
    def getTextSummary(self):
        soup = BeautifulSoup(self.post,features='html.parser').get_text()
        if len(soup) > 100:
            return soup[0:100] + '...'
        else:
            return soup

    def get_summary_post(self):
        # split first occcurence of below string and keep everything on the left
        p = self.post.split('<!-- pagebreak -->',1)[0]
        return p

    # used for search to return the number of occurrences of string
    # case is ignored
    # occurs anywhere in the text
    # compares both body of post and heading
    def occurrences(self, str_compare):
        # use beautifulsoup to only count text not html
        soup_post = BeautifulSoup(self.post).get_text()
        soup_head = BeautifulSoup(self.heading).get_text()
        return soup_post.lower().count(str_compare.lower()) + soup_head.lower().count(str_compare.lower())

    def to_dict(self, full=False):
        data = {
            'id' : self.id,
            'slug' : self.slug,
            'image_id1' : self.image_id1,
            'title' : self.title,
            'active' : self.active,
            'user' : self.user.to_dict(),
            'update_date' : self.update_date,
            'create_date' : self.create_date
        }
        if not full:
            data['summary_post'] = self.get_summary_post()
        else:
            data['post'] = self.post
        return data
    
    def __repr__(self):
        return '<Post {}>'.format(self.heading)


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    update_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    #joined means all rows returned
    #dynamic means return query objects instead of items so you can use filter
    #cascade delete-orphan means if student object is deleted then association table row is also deleted
    posts = db.relationship('Tagged',foreign_keys=[Tagged.tag_id], \
                                    backref=db.backref('tags',lazy='joined'),
                                    lazy='joined',
                                    cascade='all, delete-orphan')

    #return tag id given tag name. Return -1 if not found
    def getTagId(tag_name):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            return -1
        else:
            return tag.id

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Comment {}>'.format(self.comment)


