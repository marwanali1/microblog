import unittest

from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta


class UserModelCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        user = User(username='susan')
        user.set_password('cat')

        self.assertFalse(user.check_password('dog'))
        self.assertTrue(user.check_password('cat'))

    def test_profile_photo(self):
        user = User(username='john', email='john@example.com')
        self.assertEqual(user.profile_photo(128), 'https://www.gravatar.com/avatar/''d4c74594d841139328695756648b6bd6''?d=identicon&s=128')

    def test_follow(self):
        user_1 = User(username='susan', email='susan@example.com')
        user_2 = User(username='john', email='john@example.com')
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()
        self.assertEqual(user_1.followed.all(), [])
        self.assertEqual(user_1.followers.all(), [])

        user_1.follow(user_2)
        db.session.commit()
        self.assertTrue(user_1.is_following(user_2))
        self.assertEqual(user_1.followed.count(), 1)
        self.assertEqual(user_1.followed.first().username, 'john')
        self.assertEqual(user_2.followers.count(), 1)
        self.assertEqual(user_2.followers.first().username, 'susan')

        user_1.unfollow(user_2)
        db.session.commit()
        self.assertFalse(user_1.is_following(user_2))
        self.assertEqual(user_1.followed.count(), 0)
        self.assertEqual(user_2.followers.count(), 0)

    def test_follow_posts(self):
        # Create four test users
        user_1 = User(username='susan', email='susan@example.com')
        user_2 = User(username='john', email='john@example.com')
        user_3 = User(username='mary', email='mary@example.com')
        user_4 = User(username='david', email='david@example.com')
        db.session.add_all([user_1, user_2, user_3, user_4])

        # Create four test posts
        time_now = datetime.utcnow()
        post_1 = Post(body='Post from susan', author=user_1, timestamp=time_now + timedelta(seconds=1))
        post_2 = Post(body='Post from john', author=user_2, timestamp=time_now + timedelta(seconds=4))
        post_3 = Post(body='Post from mary', author=user_3, timestamp=time_now + timedelta(seconds=3))
        post_4 = Post(body='Post from david', author=user_4, timestamp=time_now + timedelta(seconds=2))
        db.session.add_all([post_1, post_2, post_3, post_4])
        db.session.commit()

        # Setup the followers
        user_1.follow(user_2)  # susan follows john
        user_1.follow(user_4)  # susan follows david
        user_2.follow(user_3)  # john follows mary
        user_3.follow(user_4)  # mary follows david
        db.session.commit()

        # Check the followed posts of each user
        follows_posts_1 = user_1.followed_posts().all()
        follows_posts_2 = user_2.followed_posts().all()
        follows_posts_3 = user_3.followed_posts().all()
        follows_posts_4 = user_4.followed_posts().all()

        self.assertEqual(follows_posts_1, [post_2, post_4, post_1])
        self.assertEqual(follows_posts_2, [post_2, post_3])
        self.assertEqual(follows_posts_3, [post_3, post_4])
        self.assertEqual(follows_posts_4, [post_4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
