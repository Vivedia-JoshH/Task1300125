import unittest
from app import app
from os import getenv

class FlaskAppTestCase(unittest.TestCase):
    
    def setUp(self):
        # Set up the Flask test client
        self.client = app.test_client()

if __name__ == '__main__':
    unittest.main()
