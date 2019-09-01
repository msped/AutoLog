import os
import unittest

from app import app
from utils import votes


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_response_should_success(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_builds_response_should_success(self):
        result = self.app.get('/builds')
        self.assertEqual(result.status_code, 200)

    def test_my_builds_response_should_redirect(self):
        result = self.app.get('/build/user/1')
        self.assertEqual(result.status_code, 302)

    def test_login_response_should_success(self):
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)

    def test_register_response_should_success(self):
        result = self.app.get('/register')
        self.assertEqual(result.status_code, 200)

    def test_create_response_should_redirect(self):
        result = self.app.get('/build/new')
        self.assertEqual(result.status_code, 302)

    def test_delete_response_should_redirect(self):
        result = self.app.get('/build/1/delete')
        self.assertEqual(result.status_code, 302)

    def test_register_account(self):
        """Username and email will have to be changed to test the function each
        time as it will inject a new user"""
        response = self.app.post(
            '/register',
            data=dict(
                username="test user 1",
                email="test@gmail.com",
                password="password",
                password2="password"
            ),
            follow_redirects=True
        )
        self.assertIn(b"Account created!", response.data)

    def test_register_if_account_exists(self):
        response = self.app.post(
            '/register',
            data=dict(
                username="test user 1",
                email="test@gmail.com",
                password="password",
            ),
            follow_redirects=True
        )
        self.assertIn(b"User already exists", response.data)

    def test_login_if_user_doesnt_exist(self):
        response = self.app.post(
            '/login',
            data=dict(
                email="not_a_user@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        self.assertIn(b"Incorrect E-mail/Password", response.data)

    def test_login_incorrect_password(self):
        response = self.app.post(
            '/login',
            data=dict(
                email="test_user_1@gmail.com",
                password="incorrect password"
            ),
            follow_redirects=True
        )
        self.assertIn(b"Incorrect E-mail/Password", response.data)

    def test_login_success(self):
        response = self.app.post(
            '/login',
            data=dict(
                email="test@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        self.assertIn(b"Logged in successfully", response.data)

    def test_user_logged_in_can_access_create_record(self):
        self.app.post(
            '/login',
            data=dict(
                email="test@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        result = self.app.get('/build/new')
        self.assertEqual(result.status_code, 200)

    def test_user_logged_in_can_access_my_builds(self):
        self.app.post(
            '/login',
            data=dict(
                email="test@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        """Test user ID"""
        result = self.app.get('/build/user/5d5053d52df25bd353fe7b72')
        self.assertEqual(result.status_code, 200)

    def test_utlis_function_vote_returns_true(self):
        user_email = "test@gmail.com"
        build_votes = ["test@gmail.com", "test1@gmail.com", "test3@gmail.com"]
        result = votes(user_email, build_votes)
        self.assertTrue(result)

    def test_utlis_function_vote_returns_false(self):
        user_email = "test@gmail.com",
        build_votes = ["test1@gmail.com", "test1@gmail.com", "test3@gmail.com"]
        result = votes(user_email, build_votes)
        self.assertFalse(result)

    def test_user_logged_in_can_create_record(self):
        self.app.post(
            '/login',
            data=dict(
                email="test@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        response = self.app.post(
            '/build/new',
            data=dict(
                make='Merecedes',
                model='A Class',
                trim='A45',
                year='2016',
                price='27500',
                build_name='Its a test',
                visibility='Private',
                exterior_3_product='Test Exterior Product',
                exterior_3_link='https://github.com/msped',
                exterior_3_price='100',
                total='27600'
            ),
            follow_redirects=True
        )
        self.assertIn(b"Build Created", response.data)

    def test_user_logged_in_can_access_edit(self):
        self.app.post(
            '/login',
            data=dict(
                email="test@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        response = self.app.get(
            'build/5d6916394351345d0816b05c/edit'
        )
        self.assertEqual(response.status_code, 200)

    def test_can_not_edit_other_user_build_should_redirect_to_builds(self):
        self.app.post(
            '/login',
            data=dict(
                email="test@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        response = self.app.get(
            'build/5d4b1e99beb06478ebf167e9/edit',
            follow_redirects=True
        )
        self.assertIn(b"Whoops, this isn&#39;t your build!", response.data)

    def test_can_not_delete_other_user_build_should_redirect_to_builds(self):
        self.app.post(
            '/login',
            data=dict(
                email="test@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        response = self.app.get(
            'build/5d4b1e99beb06478ebf167e9/delete',
            follow_redirects=True
        )
        self.assertIn(b"Whoops, this isn&#39;t your build!", response.data)

    def test_view_a_record(self):
        response = self.app.get(
            'build/5d6916394351345d0816b05c'
        )
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
