from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.sql import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User (db.Model):
    """ Class for storing information about users """

    # Initialize name of table
    __tablename__ = 'users'

    # Create table columns

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(15), nullable = False)
    last_name = db.Column(db.String(15), nullable = False)                
    image_url = db.Column(db.Text, nullable = False,
                          default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    
class Post(db.Model):
    """ Class for storing information about user posts """

    #Initialize name of table
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(25), nullable = False,)
    content = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref = 'posts')
    tag = db.relationship('Tag', secondary = 'post_tags', backref = 'posts' )
    post_tag = db.relationship('PostTag', backref = 'posts')


class Tag(db.Model):
    """ Class for adding tags to posts """

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False, unique = True)

class PostTag(db.Model):

    """ Class that bridges Posts and Tags """

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)
