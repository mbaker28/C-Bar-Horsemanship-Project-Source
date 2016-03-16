# PURPOSE: This file contains all of the test that are run by Shippable.

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client

class TestViews(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client = Client() # Make a test client (someone viewing the database)
    
    def test_index_view(self):
        """Tests whether the index page loads."""
        response = self.client.get("/") # e.g. http://db.cbarhorsemanship.org/
        self.assertEqual(response.status_code, 200) # Loaded...
