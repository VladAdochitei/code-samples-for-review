import unittest
import sqlite3
from src.main import app

class FlaskTestCase(unittest.TestCase):

    # Set up and tear down methods
    def setUp(self):
        # Set up a test client and initialize a test database
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        # Clean up after tests
        pass

    def test_register(self):
        response = self.app.post('/register', data=dict(
            username="testuser",
            password="password",
            confirm_password="password"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your account has been created!', response.data)

    def test_login(self):
        response = self.app.post('/login', data=dict(
            username="testuser",
            password="password"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged in successfully!', response.data)

    def test_logout(self):
        # Assuming a successful login has occurred here
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out successfully!', response.data)

    def test_user_session(self):
        # Log in to create a session
        self.app.post('/login', data=dict(username="testuser", password="password"), follow_redirects=True)
        
        # Access a route that requires a user session
        response = self.app.get('/', follow_redirects=True)
        self.assertNotIn(b'Guest', response.data)
        # Check for the presence of 'testuser' or absence of 'Guest' in the response

    def test_database_connection(self):
        try:
            conn = sqlite3.connect('messages.db')
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            self.assertIsNotNone(result)
        except sqlite3.Error as e:
            self.fail(f"SQLite error occurred: {e}")
        finally:
            conn.close()

    def test_home_page_redirect(self):
        response = self.app.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_message_sending(self):
        # This requires a logged-in session
        # Send a message
        response = self.app.post('/send_message', data=dict(message="Hello World"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Verify message is in response
        self.assertIn(b"Hello World", response.data)


import unittest
from src.main import app

class FlaskGetPagesCase(unittest.TestCase):

    # Set up and tear down methods
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_logout_page(self):
        self.app.post('/login', data=dict(username="testuser", password="password"), follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)

    def test_home_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_register_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
