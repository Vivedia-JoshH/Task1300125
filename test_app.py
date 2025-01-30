import unittest
from unittest.mock import patch
from app import app  # Import the Flask app from your script

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        """Set up a test client for the Flask app"""
        self.app = app.test_client()
        self.app.testing = True  # Enable testing mode

    @patch('app.getenv')
    def test_home_route(self, mock_getenv):
        """Test the home page response with mocked environment variables"""
        # Mock environment variables
        mock_getenv.side_effect = lambda key: "test-host" if key == "HOSTNAME" else "TestUser"

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello TestUser.", response.data)
        self.assertIn(b"I'm currently running in test-host.", response.data)

    @patch('app.getenv')
    def test_home_route_missing_env_vars(self, mock_getenv):
        """Test the home page when environment variables are missing"""
        mock_getenv.side_effect = lambda key: None  # Simulate missing vars

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello Guest.", response.data)  # Default value if USER is missing
        self.assertIn(b"I'm currently running in an unknown environment.", response.data)  # Default HOSTNAME

    @patch('app.getenv')
    def test_home_route_different_values(self, mock_getenv):
        """Test the home page with different user and hostname values"""
        mock_getenv.side_effect = lambda key: "my-server" if key == "HOSTNAME" else "Alice"

        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello Alice.", response.data)
        self.assertIn(b"I'm currently running in my-server.", response.data)

    def test_home_page_is_html(self):
        """Ensure the response is valid HTML"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.startswith(b'<!DOCTYPE html>') or b"<html" in response.data)

if __name__ == '__main__':
    unittest.main()
