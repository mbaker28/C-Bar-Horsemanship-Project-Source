# PURPOSE: This file contains all of the test that are run by Shippable.

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from  django.core.urlresolvers import reverse
from cbar_db import models
from cbar_db import forms
from cbar_db import views

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

class LiabilityReleaseForm(TestCase):
     def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)
        test_participant=models.Participant(
            name="TEST Peter Parker",
            birth_date="2016-03-31",
            email="peter@spider-man.com",
            weight="195",
            gender="M",
            guardian_name="Aunt May",
            height="72",
            minor_status="G",
            address_street="123 Apartment Street",
            address_city="New York",
            address_zip="10018",
            phone_home="(123) 456-7890",
            phone_cell_work="(444) 393-0098",
            school_institution="SHIELD"
        )
        test_participant.save()

    def test_liability_release_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching name is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Peter Parker",
            "signature": "TEST Peter Parker",
            "date": "2016-03-31"
        }
        form=forms.LiabilityReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertEquals(found_participant, True)

     def test_emergency_authorization_form_saves_with_valid_data(self):
        """ Verify that an Liability Release form view, populated with
         valid data, correctly saves the form to the database. """

        form_data={
            "name": "TEST Peter Parker",
            "signature": "TEST Peter Parker",
            "date": "2016-03-31"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-liability"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # DISABLED: We don't have a post form url redirect location or view yet
        # Assert the the redirect url matches the post-form page:
        # self.assertEqual(
        #     resp['Location'],
        #     'http://testserver/thank you place'
        # )

        # Attempt to retreive the updated MedicalInfo record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"]
            )

            print("Retrieving updated LiabilityRelease record...")
            liability_release_in_db=models.LiabilityRelease.objects.get(
                participant_id=participant_in_db,
                date=form_data["date"]
            )
            print("Successfully retrieved updated LiabilityRelease record.")
        except:
            print("ERROR: Unable to retreive updated LiabilityRelease record!")
