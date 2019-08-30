import os
import unittest

from app import app


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_status(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_builds_status(self):
        result = self.app.get('/builds')
        self.assertEqual(result.status_code, 302)

    def test_contact_status(self):
        result = self.app.get('/contact_us')
        self.assertEqual(result.status_code, 200)

    def test_login_status(self):
        result = self.app.get('/login')
        self.assertEqual(result.status_code, 200)

    def test_register_status(self):
        result = self.app.get('/register')
        self.assertEqual(result.status_code, 200)

    def test_create_status(self):
        result = self.app.get('/create_record')
        self.assertEqual(result.status_code, 302)

    def test_delete_status(self):
        result = self.app.get('/delete_record/1')
        self.assertEqual(result.status_code, 302)

    def test_register_data(self):
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

    def test_register_data(self):
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

    def test_login_exists_data(self):
        response = self.app.post(
            '/login',
            data=dict(
                email="test@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        self.assertIn(b"Logged in successfully", response.data)

    def test_login_doesnt_exist_data(self):
        response = self.app.post(
            '/login',
            data=dict(
                email="not_a_user@gmail.com",
                password="password"
            ),
            follow_redirects=True
        )
        self.assertIn(b"Incorrect E-mail/Password", response.data)

    def test_incorrect_password(self):
        response = self.app.post(
            '/login',
            data=dict(
                email="test_user_1@gmail.com",
                password="incorrect password"
            ),
            follow_redirects=True
        )
        self.assertIn(b"Incorrect E-mail/Password", response.data)

if __name__ == "__main__":
    unittest.main()
