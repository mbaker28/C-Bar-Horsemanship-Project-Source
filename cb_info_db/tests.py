# PURPOSE: This file contains all of the test that are run by Shippable.

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from  django.core.urlresolvers import reverse
from cbar_db import models
from cbar_db import forms

class TestViews(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client = Client() # Make a test client (someone viewing the database)

    def test_public_index_loads(self):
        """Tests whether the index page loads."""
        response = self.client.get(reverse('index-public'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_public_forms_index_loads(self):
        """ Tests whether the Public Forms index page loads. """
        response = self.client.get(reverse('index-public-forms'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_application_form_loads(self):
        """ Tests whether the Application form loads. """
        response = self.client.get(reverse('public-form-application'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_medical_release_form_loads(self):
        """ Tests whether the Medical Release form loads. """
        response = self.client.get(reverse('public-form-med-release'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_emergency_authorization_form_loads(self):
        """ Tests whether the Emergency Medical Treatment Authorization form
         loads. """
        response = self.client.get(reverse('public-form-emerg-auth'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_liability_release_form_loads(self):
        """ Tests whether the Liability Release form loads. """
        response = self.client.get(reverse('public-form-liability'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_media_release_form_loads(self):
        """ Tests whether the Media Release form loads. """
        response = self.client.get(reverse('public-form-media'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_background_check_form_loads(self):
        """ Tests whether the Background Check Authorization form loads. """
        response = self.client.get(reverse('public-form-backround'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_seizure_form_loads(self):
        """ Tests whether the Seizure Evaluation form loads. """
        response = self.client.get(reverse('public-form-seizure'))
        self.assertEqual(response.status_code, 200) # Loaded...

class TestForms(TestCase):
    def setUp(self):
        test_participant=models.Participant(
            name="TEST Jarvis",
            birth_date="2016-03-28",
            email="jarvis@starkenterprises.com",
            weight="170",
            gender="M",
            guardian_name="Tony Stark",
            height="72",
            minor_status="G",
            address_street="123 Stark Tower",
            address_city="New York",
            address_zip="10016",
            phone_home="(123) 456-7890",
            phone_cell_work="(444) 392-0098",
            school_institution=""
        )
        test_participant.save()

    def test_test_participant_exists(self):
        """ Test whether the test participant exists. """
        p=models.Participant.objects.get(name="TEST Jarvis")

        self.assert
