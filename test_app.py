import unittest
from app import app
from os import getenv

class FlaskAppTestCase(unittest.TestCase):
    
    def setUp(self):
        # Set up the Flask test client
        self.client = app.test_client()

       
        # Call the home route
        response = self.client.get('/')
        
        # Check if the response contains the default "friend" when YOUR_NAME is not set
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello friend.", response.data)

    def test_home_with_name(self):
        # Test the home route when 'YOUR_NAME' is set
        # Set the environment variable
        getenv('YOUR_NAME', 'Josh')
        
        # Call the home route
        response = self.client.get('/')
        
        # Check if the response contains the correct name
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello Josh.", response.data)

    def test_hostname_in_response(self):
        # Test if 'HOSTNAME' is part of the response
        # Set a sample hostname
        getenv('HOSTNAME', 'TestHost')
        
        # Call the home route
        response = self.client.get('/')
        
        # Check if the response contains the correct hostname
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"I'm currently running in TestHost.", response.data)
        
if __name__ == '__main__':
    unittest.main()
