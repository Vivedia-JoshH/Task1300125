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
        # Mock the environment variables
        mock_getenv.side_effect = lambda key: "test-host" if key == "HOSTNAME" else "TestUser"

        # Make a GET request to the home route
        response = self.app.get('/')

        # Verify the response status code
        self.assertEqual(response.status_code, 200)

        # Verify the expected content in the response
        self.assertIn(b"Hello TestUser.", response.data)
        self.assertIn(b"I'm currently running in test-host.", response.data)

if __name__ == '__main__':
    unittest.main()
