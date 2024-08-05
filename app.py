from flask import Flask, request, render_template, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.app_context().push()

# Configure the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret112'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Initialize debugging extention
debug = DebugToolbarExtension(app)

# Connect the database with flask
connect_db(app)

# Create tables if they are not already created
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

@app.route('/users')
# Get a list of all users from User class and pass it to users html
def show_users():
    users = User.query.all()
    return render_template('users.html', users = users)

@app.route('/')
# Redirects from "/" to "/users"
def redirect_to_users():
    return redirect(url_for('show_users'))

@app.route('/users/new')
# Show the page form for adding users
def show_add_user_form():
    return render_template('add_user.html')

@app.route('/users/new', methods = ['POST'])
# Gather data from the add user form.  If an image is not provided, use default image.  Pass
# information from the form to the User class and then add/commit to db.  Redirect to Users page.
def create_new_user():
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    image_url = request.form.get('image-url')

    if not image_url:
        image_url = "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('show_users'))

@app.route('/users/<int:user_id>')
# Obtain User information about the user that was selected on Users page.  Pass to User detail page.
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user = user)

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
# Get User by ID and delete from db.  Redirect to Users page
def delete_user(user_id): 
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('show_users'))

@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    # Show user edit form
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user = user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
# Get information from the form for the User and commit to db.  Redirect to Show users page.
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form.get('edit-first-name')
    user.last_name = request.form.get('edit-last-name')
    user.image_url = request.form.get('edit-image-url')

    db.session.commit()
    return redirect(url_for('show_user', user_id = user_id))

@app.route('/users/<int:user_id>/posts/new')
# Get User by user ID and pass to add_post page.
def show_add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('add_post.html', user = user, tags = tags)

@app.route('/posts/<int:post_id>')
# Get Post by Post id and pass to Post details page
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post = post)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
# Get information from new post form and add it to Post class. Add/commit to db.  Redirect to show user page.
def create_new_post(user_id):

    post_title = request.form.get('post-title')
    post_content = request.form.get('post-content')

    new_post = Post(title = post_title, content = post_content, user_id = user_id)
    db.session.add(new_post)
    db.session.commit()

    checkbox_tags = request.form.getlist('tags')

    for tag in checkbox_tags:
        new_tag = PostTag(post_id = new_post.id, tag_id = int(tag))
        db.session.add(new_tag)

    db.session.commit()
    return redirect(url_for('show_user', user_id = user_id))

@app.route('/posts/<int:post_id>/edit')
# Get Post information by post id and send to edit post page.
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    post_tags = [tag.id for tag in post.tag]
                               
    return render_template('edit_post.html', post = post, tags = tags, post_tags = post_tags)
    
@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
# Get Post information by id.  Get information from edit post form.  Commit to db.  Redirect to Show Post page
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form.get('edit-title')
    post.content = request.form.get('edit-content')

    checkbox_tags = request.form.getlist('tags')

    PostTag.query.filter_by(post_id = post_id).delete()

    for tag in checkbox_tags:
        new_tag = PostTag(post_id = post_id, tag_id = int(tag))
        db.session.add(new_tag)
    
    db.session.commit()
    return redirect(url_for('show_post', post_id = post_id))

@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
# Get Post information by id.  Delete/commit to db.  Redirect to show user.
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('show_user', user_id = post.user_id))

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/new')
def show_create_tag_form():
    return render_template('add_tag.html')

@app.route('/tags/new', methods = ['POST'])
def create_tag():

    tag_name = request.form.get('tag-name')

    tag = Tag(name = tag_name)  
    db.session.add(tag)
    db.session.commit()

    return redirect(url_for('show_tags'))


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_details.html', tag = tag)

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag = tag)

@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form.get('edit-tag-name')
    db.session.commit()

    return redirect(url_for('show_tag_details', tag_id = tag_id))

@app.route('/tags/<int:tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect(url_for('show_tags'))
    

