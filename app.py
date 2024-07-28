""" Users app to store and create User information"""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from sqlalchemy import text

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_TRACK-MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret112'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

@app.route('/')
def redirect_users():
    return redirect('/users')

@app.route('/users')
def users_list():
    users = User.query.all()
    return render_template('users.html', users = users)

@app.route('/users/new')
def show_new_user_form():
    return render_template('/new-users.html')

@app.route('/users/new', methods = ["POST"])
def create_new_user():

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    if image_url == "":
        image_url = "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = db.session.get(User, user_id)
    return render_template('user-detail.html', user = user)

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
        
        user = db.session.get(User, user_id)

        db.session.delete(user)
        db.session.commit()

        return redirect('/')


@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    user = db.session.get(User, user_id)

    return render_template('/edit-users.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def edit_user(user_id):

    edited_user = db.session.get(User, user_id)

    if edited_user:
        edited_user.first_name = request.form['edit-first-name']
        edited_user.last_name = request.form['edit-last-name']
        edited_user.image_url = request.form['edit-image-url']

    db.session.commit()

    return redirect('/')

