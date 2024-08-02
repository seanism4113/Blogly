from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_db_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class UserViewsTestCase(TestCase):
    """Tests for views for Users"""

    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        """Add sample user"""

        db.session.query(User).delete()
        db.session.query(Post).delete()

        user = User(first_name="John", last_name="Doe", image_url="https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg")
        db.session.add(user)
        db.session.commit()

        post = Post(title='Post 1', content='Content 1', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_users_page(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h3>Posts</h3>', html)
            self.assertIn('John Doe', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_add_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add Post for John Doe</h1>', html)