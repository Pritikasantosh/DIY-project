import unittest
from app import app, db
from models import User, BlogPost, Comment

class BlogPlatformTestCase(unittest.TestCase):
    """Automated Unit and Integration Tests for Flask Blogging Platform (Week 7)."""

    def setUp(self):
        """Runs before each test: initializes test client and in-memory test DB."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Runs after each test: destroys test database session."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_homepage_loads(self):
        """Verify homepage returns 200 OK."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flask', response.data)

    def test_user_registration_and_password_hashing(self):
        """Verify user signup and secure password verification."""
        with app.app_context():
            user = User(username='testdev', email='testdev@example.com')
            user.set_password('SecretPassword123')
            db.session.add(user)
            db.session.commit()

            retrieved = User.query.filter_by(username='testdev').first()
            self.assertIsNotNone(retrieved)
            self.assertTrue(retrieved.check_password('SecretPassword123'))
            self.assertFalse(retrieved.check_password('WrongPass'))

    def test_blog_post_crud(self):
        """Verify creating, reading, updating, and deleting a blog post."""
        with app.app_context():
            # Create author
            author = User(username='blogger', email='blogger@example.com')
            author.set_password('Pass123')
            db.session.add(author)
            db.session.commit()

            # Create Post (C)
            post = BlogPost(
                title='Unit Testing with Python',
                category='Programming',
                tags='python, testing',
                content='Automated tests ensure high code quality.',
                author=author
            )
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            # Read Post (R)
            fetched = db.session.get(BlogPost, post_id)
            self.assertEqual(fetched.title, 'Unit Testing with Python')
            self.assertEqual(fetched.author.username, 'blogger')

            # Update Post (U)
            fetched.title = 'Updated Title: Python Unit Testing'
            db.session.commit()
            updated = db.session.get(BlogPost, post_id)
            self.assertEqual(updated.title, 'Updated Title: Python Unit Testing')

            # Delete Post (D)
            db.session.delete(updated)
            db.session.commit()
            self.assertIsNone(db.session.get(BlogPost, post_id))

    def test_commenting_system(self):
        """Verify adding and cascading comments."""
        with app.app_context():
            user = User(username='commenter', email='commenter@example.com')
            user.set_password('Pass123')
            post = BlogPost(title='Discussion Post', content='Content here', author=user)
            db.session.add_all([user, post])
            db.session.commit()

            comment = Comment(content='Insightful article!', author=user, post=post)
            db.session.add(comment)
            db.session.commit()

            self.assertEqual(len(post.comments), 1)
            self.assertEqual(post.comments[0].content, 'Insightful article!')

    def test_custom_404_error_page(self):
        """Verify accessing a nonexistent route renders our custom 404 page."""
        response = self.client.get('/nonexistent-page-url-xyz')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)
        self.assertIn(b'404', response.data)

    def test_search_and_category_filtering(self):
        """Verify search query logic filters properly."""
        with app.app_context():
            user = User(username='author2', email='author2@example.com')
            user.set_password('Pass123')
            p1 = BlogPost(title='Flask Deployment', content='Deploy to cloud', category='Technology', tags='cloud', author=user)
            p2 = BlogPost(title='Healthy Eating', content='Food and wellness', category='Lifestyle', tags='food', author=user)
            db.session.add_all([user, p1, p2])
            db.session.commit()

        # Search for keyword
        res = self.client.get('/?q=Deployment')
        self.assertIn(b'Flask Deployment', res.data)
        self.assertNotIn(b'Healthy Eating', res.data)

        # Filter by category
        res_cat = self.client.get('/?category=Lifestyle')
        self.assertIn(b'Healthy Eating', res_cat.data)
        self.assertNotIn(b'Flask Deployment', res_cat.data)

if __name__ == '__main__':
    unittest.main()
