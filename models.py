from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User (db.Model):
    """ Class for storing information about users """

    # Initialize name of table
    __tablename__ = "users"

    # Create table columns

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.String(15),
                           nullable = False)

    last_name = db.Column(db.String(15),
                           nullable = False)                

    image_url = db.Column(db.String(255),
                          nullable = False;
                          default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')