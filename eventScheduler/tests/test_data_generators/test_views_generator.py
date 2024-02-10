import unittest
from .views_generator import *

class TestViewDataClasses(unittest.TestCase):
    def test_user_data_initialization(self):
        user_data = UserData().data
        self.assertIsNotNone(user_data['guid'])
        self.assertEqual(user_data['first_name'], 'random-first-name')
        self.assertEqual(user_data['last_name'], 'random-last-name')
        self.assertEqual(user_data['email'], 'random@something.com')
        self.assertEqual(user_data['image'], 'random-image-url')
        self.assertIsNotNone(user_data['organization_id'])

    def test_request_format(self):
        request_data = UserData().request_format()
        self.assertNotIn('guid', request_data)
        self.assertIn('first_name', request_data)

    def test_server_response_format(self):
        user_data = UserData()
        response_data = user_data.server_response_format()
        self.assertIn('guid', response_data)
        self.assertEqual(response_data, user_data.data)

    def test_missing(self):
        user_data = UserData()
        missing_data = user_data.missing('first_name', 'image')
        self.assertNotIn('first_name', missing_data)
        self.assertNotIn('image', missing_data)
        self.assertIn('guid', missing_data)
        self.assertIn('last_name', missing_data)
