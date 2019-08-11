import os 
import unittest

from app import app

class testCase(unittest.TestCase):

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
    
    # Page Status - Builds, create record both have @login_required, 302 redirect will be returned.
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

if __name__ == "__main__":
    unittest.main()
