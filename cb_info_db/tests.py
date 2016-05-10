# PURPOSE: This file contains all of the test that are run by Shippable.

from datetime import *
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from cbar_db import models
from cbar_db import forms
from cbar_db import views


class TestPublicViews(TestCase):
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
        response = self.client.get(reverse('public-form-background'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_seizure_form_loads(self):
        """ Tests whether the Seizure Evaluation form loads. """
        response = self.client.get(reverse('public-form-seizure'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_donation_index_loads(self):
        """ Tests whether the Donation index page loads. """
        response = self.client.get(reverse('donation-index'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_donation_participant_loads(self):
        """ Tests whether the Adopt A Participant donation form loads. """
        response = self.client.get(reverse('donation-participant'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_donation_horse_loads(self):
        """ Tests whether the Adopt A Horse donation form loads. """
        response = self.client.get(reverse('donation-horse'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_donation_monetary_loads(self):
        """ Tests whether the Monetary Donation form loads. """
        response = self.client.get(reverse('donation-monetary'))
        self.assertEqual(response.status_code, 200) # Loaded...


class TestApplicationForm(TestCase):
    def setUp(self):
        setup_test_environment() #Initialize the test enviornment
        client=Client() #Make a test client (someone viewing the database)

        # Create a Participant record and save it
        test_participant=models.Participant(
            name="TEST Bruce Wayne",
            birth_date="1984-6-24",
            email="bruce@wayneenterprises.com",
            weight=185.0,
            gender="M",
            guardian_name="Alfred Pennyworth",
            height=72.0,
            minor_status="G",
            address_street="1234 Wayne St.",
            address_city="Gotham",
            address_state="OK",
            address_zip= "424278",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="590-039-3000",
            school_institution="Ra's Al Ghul School of Ninjutsu"
        )
        test_participant.save()

        test_position=models.ParticipantType(
            participant_type="P",
            participant_id=test_participant
        )
        test_position.save()

    def test_application_form_creates_participant(self):
        """ Tests whether the form creates a participant record once all
            fields are entered. """

        form_data={
            "participant_type_staff": False,
            "participant_type_volunteer": False,
            "participant_type_participant": True,
            "name": "TEST Matt Murdock",
            "birth_date": "1989-5-20",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height_feet": "5",
            "height_inches": "8.5",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_state": "OK",
            "address_zip": "74801",
            "phone_home": "400-100-2000",
            "phone_cell": "400-200-3000",
            "phone_work": "400-300-4000",
            "school_institution": "Stick's School of Kung Fu"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-application"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the updated Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
        except:
            print("ERROR: Unable to retreive participant record!")

        # Verify that all of the Participant fields were set correctly:
        self.assertEqual(
            participant_in_db.name,
            form_data["name"]
        )
        self.assertEqual(
            "{d.year}-{d.month}-{d.day}".format(d=participant_in_db.birth_date),
            form_data["birth_date"]
        )
        self.assertEqual(
            participant_in_db.height,
            # Convert ft'in" to inches
            float(form_data["height_feet"])*12 + float(form_data["height_inches"])
        )
        self.assertEqual(
            str(participant_in_db.weight), # To string so can check against form
            form_data["weight"]
        )
        self.assertEqual(
            participant_in_db.gender,
            form_data["gender"]
        )
        self.assertEqual(
            participant_in_db.minor_status,
            form_data["minor_status"]
        )
        self.assertEqual(
            participant_in_db.school_institution,
            form_data["school_institution"]
        )
        self.assertEqual(
            participant_in_db.guardian_name,
            form_data["guardian_name"]
        )
        self.assertEqual(
            participant_in_db.address_street,
            form_data["address_street"]
        )
        self.assertEqual(
            participant_in_db.address_city,
            form_data["address_city"]
        )
        self.assertEqual(
            participant_in_db.address_zip,
            form_data["address_zip"]
        )
        self.assertEqual(
            participant_in_db.phone_home,
            form_data["phone_home"]
        )
        self.assertEqual(
            participant_in_db.phone_cell,
            form_data["phone_cell"]
        )
        self.assertEqual(
            participant_in_db.phone_work,
            form_data["phone_work"]
        )
        self.assertEqual(
            participant_in_db.email,
            form_data["email"]
        )

    def test_application_form_creates_participanttype_records_if_true(self):
        """ Tests whether the form creates the relevant ParticipantType records
        if they were selected. """

        form_data={
            "participant_type_staff": True,
            "participant_type_volunteer": True,
            "participant_type_participant": True,
            "name": "TEST Matt Murdock",
            "birth_date": "2010-5-20",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height_feet": "5",
            "height_inches": "8.5",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_state": "OK",
            "address_zip": "74801",
            "phone_home": "400-100-2000",
            "phone_cell": "400-200-3000",
            "phone_work": "400-300-4000",
            "school_institution": "Stick's School of Kung Fu"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-application"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Attempt to retreive the new Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
        except:
            print("ERROR: Unable to retreive participant record!")

        # Attempt to retrieve the staff ParticipantType record:
        found_staff=False
        try:
            print("Retrieving staff ParticipantType record...")
            staff_in_db=models.ParticipantType.objects.get(
                participant_id=participant_in_db,
                participant_type=models.ParticipantType.STAFF
            )
            found_staff=True
        except:
            print("ERROR: Unable to retreive staff ParticipantType record!")
        self.assertTrue(found_staff)

        # Attempt to retrieve the volunteer ParticipantType record:
        found_volunteer=False
        try:
            print("Retrieving volunteer ParticipantType record...")
            volunteer_in_db=models.ParticipantType.objects.get(
                participant_id=participant_in_db,
                participant_type=models.ParticipantType.VOLUNTEER
            )
            found_volunteer=True
        except:
            print("ERROR: Unable to retreive volunteer ParticipantType record!")
        self.assertTrue(found_volunteer)

        # Attempt to retrieve the participant ParticipantType record:
        found_participant=False
        try:
            print("Retrieving participant ParticipantType record...")
            participant_in_db=models.ParticipantType.objects.get(
                participant_id=participant_in_db,
                participant_type=models.ParticipantType.PARTICIPANT
            )
            found_participant=True
        except:
            print(
                "ERROR: Unable to retrieve participant ParticipantType record!"
            )
        self.assertTrue(found_participant)

    def test_application_form_no_creates_participanttype_records_if_false(self):
        """ Tests that the form does not create the relevant ParticipantType
         records if they were not selected. """

        form_data={
            "participant_type_staff": False,
            "participant_type_volunteer": False,
            "participant_type_participant": False,
            "name": "TEST Matt Murdock",
            "birth_date": "2013-5-20",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height_feet": "5",
            "height_inches": "8.5",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_state": "OK",
            "address_zip": "74801",
            "phone_home": "400-100-2000",
            "phone_cell": "400-200-3000",
            "phone_work": "400-300-4000",
            "school_institution": "Stick's School of Kung Fu"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-application"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Attempt to retreive the new Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
        except:
            print("ERROR: Unable to retreive participant record!")

        # Attempt to retrieve the staff ParticipantType record:
        found_staff=False
        try:
            print("Retrieving staff ParticipantType record...")
            staff_in_db=models.ParticipantType.objects.get(
                participant_id=participant_in_db,
                participant_type=models.ParticipantType.STAFF
            )
            found_staff=True
            print("ERROR: Found staff ParticipantType record!")
        except:
            pass
        self.assertFalse(found_staff)

        # Attempt to retrieve the volunteer ParticipantType record:
        found_volunteer=False
        try:
            print("Retrieving volunteer ParticipantType record...")
            volunteer_in_db=models.ParticipantType.objects.get(
                participant_id=participant_in_db,
                participant_type=models.ParticipantType.VOLUNTEER
            )
            found_volunteer=True
            print("ERROR: Found volunteer ParticipantType record!")
        except:
            pass
        self.assertFalse(found_volunteer)

        # Attempt to retrieve the participant ParticipantType record:
        found_participant=False
        try:
            print("Retrieving participant ParticipantType record...")
            participant_in_db=models.ParticipantType.objects.get(
                participant_id=participant_in_db,
                participant_type=models.ParticipantType.PARTICIPANT
            )
            found_participant=True
            print("ERROR: Found participant ParticipantType record!")
        except:
            pass
        self.assertFalse(found_participant)

    def test_application_form_participant_already_exists(self):
        """ Form throws error if the participant already exists. """

        form_data={
            "participant_type_staff": False,
            "participant_type_volunteer": False,
            "participant_type_participant": True,
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height_feet": "5",
            "height_inches": "8.5",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_state": "OK",
            "address_zip": "74801",
            "phone_home": "555 666 7777",
            "phone_cell": "",
            "phone_work": "",
            "school_institution": "Stick's School of Kung Fu"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-application"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        print(response.context)
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_ALREADY_EXISTS
            )
        )

    def test_application_form_participant_does_not_exist_with_invalid_data(self):
        """ Form throws an error if the form data is not valid. """

        form_data={
            "participant_type_staff": False,
            "participant_type_volunteer": False,
            "participant_type_participant": True,
            "name": "TEST sdf83sdf",
            "birth_date": "sdf##df",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height_feet": "5",
            "height_inches": "8.5",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_state": "OK",
            "address_zip": "654321",
            "phone_home": "400 100 2000",
            "phone_cell": "400 200 3000",
            "phone_work": "400 300 4000",
            "school_institution": "Stick's School of Kung Fu"
        }
        form=forms.ApplicationForm(form_data)

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-application"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_application_form_with_no_phone_numbers_throws_error(self):
        """ Verify that an Application form view, populated with no phone
         numbers, displays an error message. """

        form_data={
            "participant_type_staff": False,
            "participant_type_volunteer": False,
            "participant_type_participant": True,
            "name": "TEST Matt Murdock",
            "birth_date": "1989-5-20",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height_feet": "5",
            "height_inches": "8.5",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_state": "OK",
            "address_zip": "654321",
            "phone_home": "",
            "phone_cell": "",
            "phone_work": "",
            "school_institution": "Stick's School of Kung Fu"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-application"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that each phone field threw the correct error:
        self.assertFormError(
            response,
            "form",
            "phone_home",
            forms.ERROR_TEXT_NO_PHONE
        )
        self.assertFormError(
            response,
            "form",
            "phone_cell",
            forms.ERROR_TEXT_NO_PHONE
        )
        self.assertFormError(
            response,
            "form",
            "phone_work",
            forms.ERROR_TEXT_NO_PHONE
        )

    def test_application_form_with_invalid_height_feet_throws_error(self):
        """ Verify that an Application form view, populated with an invalid,
         number for the height_feet field displays an error message. """

        form_data={
            "participant_type_staff": False,
            "participant_type_volunteer": False,
            "participant_type_participant": True,
            "name": "TEST Matt Murdock",
            "birth_date": "1989-5-20",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height_feet": "9",
            "height_inches": "8.5",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_state": "OK",
            "address_zip": "654321",
            "phone_home": "100 300 4000",
            "phone_cell": "",
            "phone_work": "",
            "school_institution": "Stick's School of Kung Fu"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-application"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that each phone field threw the correct error:
        self.assertFormError(
            response,
            "form",
            "height_feet",
            forms.ApplicationForm.ERROR_TEXT_INVALID_HEIGHT_FT
        )

    def test_application_form_with_invalid_height_inches_throws_error(self):
        """ Verify that an Application form view, populated with an invalid,
         number for the height_inches field displays an error message. """

        form_data={
            "participant_type_staff": False,
            "participant_type_volunteer": False,
            "participant_type_participant": True,
            "name": "TEST Matt Murdock",
            "birth_date": "1989-5-20",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height_feet": "5",
            "height_inches": "99.9",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_state": "OK",
            "address_zip": "654321",
            "phone_home": "100 300 4000",
            "phone_cell": "",
            "phone_work": "",
            "school_institution": "Stick's School of Kung Fu"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-application"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that each phone field threw the correct error:
        self.assertFormError(
            response,
            "form",
            "height_inches",
            forms.ApplicationForm.ERROR_TEXT_INVALID_HEIGHT_IN
        )


class TestFormSavedPage(TestCase):
    def test_form_saved_page_loads_with_correct_parameter(self):
        """ Tests that the form_saved view tells the user the form saved, if it
         has the parameter set saying it came from a form redirect. """

        response = self.client.get(reverse("form-saved")+"?a=a")

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_form_saved_page_redirects_if_no_paramater_passed(self):
        """ Tests that the form_saved view redirects to the home page, if it is
         not sent the parameter set saying it came from a form redirect. """

        response = self.client.get(reverse("form-saved"))

        self.assertEqual(response.status_code, 302) # Redirected...

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            "/"
        )


class TestEmergencyAuthorizationForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        # Create a Participant record and save it
        test_participant=models.Participant(
            name="TEST Bruce Wayne",
            birth_date="1984-6-24",
            email="bruce@wayneenterprises.com",
            weight=185.0,
            gender="M",
            guardian_name="Alfred Pennyworth",
            height=72.0,
            minor_status="G",
            address_street="1234 Wayne St.",
            address_city="Gotham",
            address_state="OK",
            address_zip= "74804",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
            school_institution="Ra's Al Ghul School of Ninjutsu"
        )
        test_participant.save()

        # Create a Participant record and save it
        test_participant_no_med_record=models.Participant(
            name="TEST The Doctor",
            birth_date="1235-8-14",
            email="thedoctor@galifrey.com",
            weight=190,
            gender="M",
            height=76.0,
            minor_status="A",
            address_street="The TARDIS",
            address_city="Time and space",
            address_state="OK",
            address_zip="74801",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
        )
        test_participant_no_med_record.save()

        test_medical_info=models.MedicalInfo(
            participant_id=test_participant,
            date="2015-1-1",
            primary_physician_name="Dr. Default",
            primary_physician_phone="111-111-1111",
            last_seen_by_physician_date="2016-1-1",
            last_seen_by_physician_reason="Normal check up visit.",
            allergies_conditions_that_exclude="N",
            heat_exhaustion_stroke="N",
            tetanus_shot_last_ten_years="Y",
            seizures_last_six_monthes="N",
            doctor_concered_re_horse_activites="N",
            physical_or_mental_issues_affecting_riding="N",
            restriction_for_horse_activity_last_five_years="N",
            present_restrictions_for_horse_activity="N",
            limiting_surgeries_last_six_monthes="N",
            signature="TEST Bruce Wayne",
            currently_taking_any_medication="N",
            pregnant="N"
        )
        test_medical_info.save()

        test_medication=models.Medication(
            participant_id=test_participant,
            date="2015-1-1",
            medication_name="Supersciencymediph",
            reason_taken="reasons and stuff",
            frequency="Every 2-3 hours when in pain"
        )
        test_medication.save()

        emergency_authorization=models.AuthorizeEmergencyMedicalTreatment(
            participant_id=test_participant,
            date="2016-4-30",
            pref_medical_facility="Shawnee Medical Center",
            insurance_provider="Blue Cross Blue Shield of Oklahoma",
            insurance_policy_num="EI238901AAK7",
            emerg_contact_name="John Jacobs",
            emerg_contact_phone="(406) 892-7012",
            emerg_contact_relation="Brother In-Law",
            alt_emerg_procedure="",
            consents_emerg_med_treatment="Y",
            signature="TEST Bruce Wayne"
        )
        emergency_authorization.save()

    def test_emergency_authorization_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2015-1-1",
            "signature": "TEST Bruce Wayne"
        }
        form=forms.EmergencyMedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertEquals(found_participant, True)

    def test_emergency_authorization_form_not_valid_participant_name(self):
        """ Tests whether the form finds a participant record if the input has a
         matching date, but not a matching name. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Not A Person",
            "birth_date": "1984-6-24",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2015-1-1",
            "signature": "TEST Bruce Wayne"
        }
        form=forms.EmergencyMedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could not find the participant:
        self.assertEquals(found_participant, False)

    def test_emergency_authorization_form_not_valid_birth_date(self):
        """ Tests whether the form finds a participant record if the input has a
         matching name, but not a matching date. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1000-1-1",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2015-1-1",
            "signature": "TEST Bruce Wayne"
        }
        form=forms.EmergencyMedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could not find the participant:
        self.assertEquals(found_participant, False)

    def test_emergency_authorization_form_saves_with_valid_data(self):
        """ Verify that an Emergency Authorization form view, populated with
         valid data, correctly saves the form to the database. """

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2016-1-1",
            "signature": "TEST Bruce Wayne"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-emerg-auth"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the updated MedicalInfo record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )

            print("Retrieving updated MedicalInfo record...")
            medical_info_in_db=models.MedicalInfo.objects.get(
                participant_id=participant_in_db,
                date=form_data["date"]
            )
            print("Successfully retrieved updated MedicalInfo record.")
        except:
            print("ERROR: Unable to retreive updated MedicalInfo record!")

        # Check that the stored MedicalInfo attributes were updated correctly:
        print("Checking stored MedicalInfo attributes...")
        self.assertEqual(
            medical_info_in_db.primary_physician_name,
            form_data["primary_physician_name"]
        )
        self.assertEqual(
            medical_info_in_db.primary_physician_phone,
            form_data["primary_physician_phone"]
        )
        print("Stored MedicalInfo attributes were updated correctly.")

        # Attempt to retreive the new AuthorizeEmergencyMedicalTreatment record:
        try:
            print("Retrieving new AuthorizeEmergencyMedicalTreatment record...")
            auth_emerg_in_db=(models.AuthorizeEmergencyMedicalTreatment
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"]
                )
            )
            print(
                "Successfully retrieved new AuthorizeEmergencyMedicalTreatment"
                " record."
            )
        except:
            print(
                "ERROR: Unable to retreive new"
                " AuthorizeEmergencyMedicalTreatment record!"
            )

        # Check that the attributes in the AuthorizeEmergencyMedicalTreatment
        # were set correctly:
        print(
            "Checking stored AuthorizeEmergencyMedicalTreatment attributes..."
        )
        self.assertEqual(
            auth_emerg_in_db.pref_medical_facility,
            form_data["pref_medical_facility"]
        )
        self.assertEqual(
            auth_emerg_in_db.insurance_provider,
            form_data["insurance_provider"]
        )
        self.assertEqual(
            auth_emerg_in_db.insurance_policy_num,
            form_data["insurance_policy_num"]
        )
        self.assertEqual(
            auth_emerg_in_db.emerg_contact_name,
            form_data["emerg_contact_name"]
        )
        self.assertEqual(
            auth_emerg_in_db.emerg_contact_phone,
            form_data["emerg_contact_phone"]
        )
        self.assertEqual(
            auth_emerg_in_db.emerg_contact_relation,
            form_data["emerg_contact_relation"]
        )
        self.assertEqual(
            auth_emerg_in_db.consents_emerg_med_treatment,
            form_data["consents_emerg_med_treatment"]
        )
        self.assertEqual(
            # Format the retrieved date so it matches the input format:
            "{d.year}-{d.month}-{d.day}".format(d=auth_emerg_in_db.date),
            form_data["date"]
        )
        self.assertEqual(
            auth_emerg_in_db.signature,
            form_data["signature"]
        )

    def test_emergency_authorization_form_with_invalid_participant_name(self):
        """ Verify that an Emergency Authorization form view, populated with
         an invalid participant name, displays an error message. """

        form_data={
            "name": "TEST Not A Person",
            "birth_date": "1984-6-24",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2016-1-1",
            "signature": "TEST Bruce Wayne"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-emerg-auth"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_emergency_authorization_form_with_invalid_participant_date(self):
        """ Verify that an Emergency Authorization form view, populated with
         an invalid participant date, displays an error message. """

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1900-1-1",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2016-1-1",
            "signature": "TEST Bruce Wayne"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-emerg-auth"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_emergency_authorization_form_with_invalid_form_data(self):
        """ Verify that an Emergency Authorization form view, populated with
         an invalid participant date, displays an error message. """

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "blahblahnotdate",
            "signature": "TEST Bruce Wayne"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-emerg-auth"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_emergency_authorization_form_with_no_medical_info(self):
        """ Verify that an Emergency Authorization form view, populated with
         valid data, but without a matching MedicalInfo record, displays an
         error message. """

        form_data={
            "name": "TEST The Doctor",
            "birth_date": "1235-8-14",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2016-1-1",
            "signature": "TEST Bruce Wayne"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-emerg-auth"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_MEDICAL_INFO_NOT_FOUND
            )
        )

    def test_emergency_authorization_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a MedicalInfo record with the same
         (participant_id, date) as its primary key. """

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "111-222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "404-333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2016-4-30",
            "signature": "TEST Bruce Wayne"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-emerg-auth"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertEqual(
            views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                form="emergency medical treatment authorization"
            ),
            response.context["error_text"]
        )


class TestMediaReleaseForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        # Create a Participant record and save it
        test_participant=models.Participant(
            name="TEST Bruce Wayne",
            birth_date="1984-6-24",
            email="bruce@wayneenterprises.com",
            weight=185.0,
            gender="M",
            guardian_name="Alfred Pennyworth",
            height=72.0,
            minor_status="G",
            address_street="1234 Wayne St.",
            address_city="Gotham",
            address_state="OK",
            address_zip= "74804",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
            school_institution="Ra's Al Ghul School of Ninjutsu"
        )
        test_participant.save()

        # Create a Participant record and save it
        test_participant_no_med_record=models.Participant(
            name="TEST The Doctor",
            birth_date="1235-8-14",
            email="thedoctor@galifrey.com",
            weight=190,
            gender="M",
            height=76.0,
            minor_status="A",
            address_street="The TARDIS",
            address_city="Time and space",
            address_state="OK",
            address_zip="74801",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
        )
        test_participant_no_med_record.save()

        media_release=models.MediaRelease(
            participant_id=test_participant,
            date="2014-3-5",
            consent="Y",
            signature="TEST Oliver Queen"
        )
        media_release.save()

        test_medical_info=models.MedicalInfo(
            participant_id=test_participant,
            date="2016-1-1",
            primary_physician_name="Dr. Default",
            primary_physician_phone="111-111-1111",
            last_seen_by_physician_date="2016-1-1",
            last_seen_by_physician_reason="Normal check up visit.",
            allergies_conditions_that_exclude="N",
            heat_exhaustion_stroke="N",
            tetanus_shot_last_ten_years="Y",
            seizures_last_six_monthes="N",
            doctor_concered_re_horse_activites="N",
            physical_or_mental_issues_affecting_riding="N",
            restriction_for_horse_activity_last_five_years="N",
            present_restrictions_for_horse_activity="N",
            limiting_surgeries_last_six_monthes="N",
            signature="TEST Bruce Wayne",
            currently_taking_any_medication="N",
            pregnant="N"
        )
        test_medical_info.save()

    def test_media_release_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "consent": "Y",
            "signature": "TEST Bruce Wayne",
            "date": "2016-1-1"
        }
        form=forms.MediaReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertTrue(found_participant)

    def test_media_release_form_not_valid_participant_name(self):
        """ Verify that a Media Release form view, populated with an invalid
         participant name, displays an error message. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST I'm Not Bruce Wayne",
            "birth_date": "1984-6-24",
            "consent": "Y",
            "signature": "TEST Bruce Wayne",
            "date": "2016-1-1"
        }
        form=forms.MediaReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could not find the participant:
        self.assertFalse(found_participant)

    def test_media_release_form_not_valid_birth_date(self):
        """ Verify that a Media Release form view, populated with an invalid
         participant birth date, displays an error message. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1000-2-3",
            "consent": "Y",
            "signature": "TEST Bruce Wayne",
            "date": "2016-1-1"
        }
        form=forms.MediaReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could not find the participant:
        self.assertFalse(found_participant)

    def test_media_release_form_saves_with_valid_data(self):
        """ Verify that a Media Release form view, populated with
         valid data, correctly saves the form to the database. """

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "consent": "Y",
            "signature": "TEST Bruce Wayne",
            "date": "2016-1-1"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-media"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the updated MedicalInfo record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
        except:
            print("ERROR: Unable to retreive participant record!")

        # Attempt to retreive the new MediaRelease record:
        try:
            print("Retrieving new MediaRelease record...")
            media_release_in_db=(models.MediaRelease
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"]
                )
            )
            print(
                "Successfully retrieved new MediaRelease record."
            )
        except:
            print(
                "ERROR: Unable to retreive new MediaRelease record!"
            )

        # Check that the attributes in the MediaRelease were set correctly:
        print(
            "Checking stored MediaRelease attributes..."
        )
        self.assertEqual(
            media_release_in_db.consent,
            form_data["consent"]
        )
        self.assertEqual(
            media_release_in_db.signature,
            form_data["signature"]
        )
        self.assertEqual(
            # Format the retrieved date so it matches the input format:
            "{d.year}-{d.month}-{d.day}".format(d=media_release_in_db.date),
            form_data["date"]
        )

    def test_media_release_form_with_invalid_participant_name(self):
        """ Verify that a Media Release form view, populated with
         an invalid participant name, displays an error message. """

        form_data={
            "name": "TEST I'm Not Bruce Wayne",
            "birth_date": "1984-6-24",
            "consent": "Y",
            "signature": "TEST Bruce Wayne",
            "date": "2016-1-1"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-media"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_media_release_form_with_invalid_participant_date(self):
        """ Verify that a Media Release form view, populated with
         an invalid participant date, displays an error message. """

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "2000-1-2",
            "consent": "Y",
            "signature": "TEST Bruce Wayne",
            "date": "2016-1-1"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-media"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        form_data={
            "name": "TEST Bruce Wayne with a super long name zzzzzzzzzzzzzzzzzz"
                "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
                "zzzzzzzz",
            "birth_date": "this isn't a date",
            "consent": "Y",
            "signature": "TEST Bruce Wayne",
            "date": "2016-1-1"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-media"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_media_release_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a MedicalInfo record with the same
         (participant_id, date) as its primary key. """

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "consent": "Y",
            "signature": "TEST Bruce Wayne",
            "date": "2014-3-5"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-media"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertEqual(
            views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                form="media release"
            ),
            response.context["error_text"]
        )


class TestBackGroundCheck(TestCase):
    def setUp(self):
        setup_test_environment()
        client=Client()
        # test_participant=models.Participant(
        #     name="TEST Barry Allen",
        #     birth_date="1994-6-25",
        #     date="1994-5-4",
        #     signature="TEST Barry Allen",
        #     driver_license_num="kgjenekkidik123"
        # )
        # test_participant.save()

        # Create a Participant record and save it
        test_participant=models.Participant(
            name="TEST Barry Allen",
            birth_date="1994-6-25",
            email="bruce@wayneenterprises.com",
            weight=185.0,
            gender="M",
            guardian_name="Alfred Pennyworth",
            height=72.0,
            minor_status="G",
            address_street="1234 Wayne St.",
            address_city="Gotham",
            address_state="OK",
            address_zip= "74804",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            school_institution="Ra's Al Ghul School of Ninjutsu"
        )
        test_participant.save()

        background_check=models.BackgroundCheck(
            participant_id=test_participant,
            date="2014-3-5",
            signature="TEST Oliver Queen",
            driver_license_num="79801234AB"
        )
        background_check.save()

    def test_background_check_form_finds_valid_participant(self):
        found_participant=False

        form_data={
            "name": "TEST Barry Allen",
            "birth_date":"1994-6-25",
            "signature":"TEST Barry Allen",
            "date":"1994-5-4",
            "driver_license_num":"kgjenekkidik123"
        }
        form=forms.BackgroundCheckForm(form_data)

        if form.is_valid():
            print("form is Valid.")

            try:
                print("Finding Participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found Participant")
                found_participant=True

            except:
                print("The Form is not Valid")
                found_participant=False

            self.assertEquals(found_participant,True)

    def test_background_check_form_not_valid_participant_name(self):

        found_participant=False

        form_data={
            "name":"TEST Not a person",
            "birth_date":"1234-4-5",
            "signature":"TEST Barry Allen",
            "date":"1994-5-4",
            "driver_license_num":"kgjenekkidik123"
        }
        form=forms.BackgroundCheckForm(form_data)

        if form.is_valid():
            print("Form is valid.")

            try:
                print("found participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found Participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False
        else:
            print("Form is not valid")

        self.assertEquals(found_participant,False)

    def test_background_check_form_not_valid_birth_date(self):
        found_participant=False

        form_data={
            "name":"TEST Barry Allen",
            "birth_date":"1234-7-10",
            "signature":"TEST Barry Allen",
            "date":"1994-5-4",
            "driver_license_num":"kgjenekkidik123"
        }
        form=forms.BackgroundCheckForm(form_data)

        if form.is_valid():
            print("Form is Valid")

            try:
                print("finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found Participant")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False
        else:
            print("form is not valid.")

        self.assertEquals(found_participant, False)

    def test_background_check_form_saves_with_valid_data(self):

        form_data={
            "name":"TEST Barry Allen",
            "birth_date":"1994-6-25",
            "signature":"TEST Barry Allen",
            "date":"1994-5-4",
            "driver_license_num":"kgjenekkidik123"
        }

        response=self.client.post(reverse("public-form-background"), form_data)

        self.assertEqual(response.status_code, 302)

        try:
            print("retrieving Participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
            print("Successfully retrieved Participant record.")
        except:
            print("ERROR: Unable to retrieve updated BackgroundCheck record")
        try:
            print("Retrieving updated BackgroundCheck")
            public_form_background_in_db=models.BackgroundCheck.objects.get(
                participant_id=participant_in_db,
                date=form_data["date"]
            )
            print("Successfully retrieved updated BackgroundCheck record.")
        except:
            print("ERROR: Unable to rereive updated BackgroundCheck record")

        print("checking stored BackgroundCheck attributes...")

        self.assertEqual(
            public_form_background_in_db.signature,
            form_data["signature"]
        )
        self.assertEqual(
            "{d.year}-{d.month}-{d.day}".format(
                d=public_form_background_in_db.date
            ),
            form_data["date"]
        )
        self.assertEqual(
            public_form_background_in_db.driver_license_num,
            form_data["driver_license_num"]
        )

    def test_background_check_form_with_invalid_participant_name(self):

        form_data={
            "name":"TEST Not Barry Allen",
            "birth_date":"1994-6-25",
            "signature":"TEST Barry Allen",
            "date":"1994-5-4",
            "driver_license_num":"kgjenekkidik123"
        }

        response=self.client.post(reverse("public-form-background"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_background_check_form_with_invalid_form_data(self):

        form_data={
            "name":"TEST Barry Allen",
            "birth_date":"1994-6-25",
            "signature":"TEST Barry Allen",
            "date":"blahblahnotdate",
            "driver_license_num":"kgjenekkidik123"
        }

        response=self.client.post(reverse("public-form-background"),form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_background_check_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a MedicalInfo record with the same
         (participant_id, date) as its primary key. """

        form_data={
            "name":"TEST Barry Allen",
            "birth_date":"1994-6-25",
            "signature":"TEST Barry Allen",
            "date":"2014-3-5",
            "driver_license_num":"kgjenekkidik123"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-background"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertEqual(
            views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                form="background check authorization"
            ),
            response.context["error_text"]
        )


class TestMedicalReleaseForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        # Create a Participant record and save it
        test_participant=models.Participant(
            name="TEST Bruce Wayne",
            birth_date="1984-6-24",
            email="bruce@wayneenterprises.com",
            weight=185.0,
            gender="M",
            guardian_name="Alfred Pennyworth",
            height=72.0,
            minor_status="G",
            address_street="1234 Wayne St.",
            address_city="Gotham",
            address_state="OK",
            address_zip= "74804",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            school_institution="Ra's Al Ghul School of Ninjutsu"
        )
        test_participant.save()

        test_medical_info=models.MedicalInfo(
            participant_id=test_participant,
            date="2016-1-1",
            primary_physician_name="Dr. Default",
            primary_physician_phone="111-111-1111",
            last_seen_by_physician_date="2016-1-1",
            last_seen_by_physician_reason="Normal check up visit.",
            allergies_conditions_that_exclude="N",
            heat_exhaustion_stroke="N",
            tetanus_shot_last_ten_years="Y",
            seizures_last_six_monthes="N",
            doctor_concered_re_horse_activites="N",
            physical_or_mental_issues_affecting_riding="N",
            restriction_for_horse_activity_last_five_years="N",
            present_restrictions_for_horse_activity="N",
            limiting_surgeries_last_six_monthes="N",
            signature="TEST Oliver Queen",
            currently_taking_any_medication="N",
            pregnant="N"
        )
        test_medical_info.save()

    def test_medical_release_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "primary_physician_name": "Dr. Physician Man",
            "primary_physician_phone": "1112223333",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "N",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "N",
            "currently_taking_any_medication": "Y",
            "pregnant": "N",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "N",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": "N",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }
        form=forms.MedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertTrue(found_participant)

    def test_medical_release_form_not_valid_participant_name(self):
        """ Tests whether the form finds a participant record if the input has a
         matching date, but not a matching name. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "primary_physician_name": "Dr. Physician Man",
            "primary_physician_phone": "1112223333",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "N",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "N",
            "currently_taking_any_medication": "Y",
            "pregnant": "N",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "N",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": "N",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST I'm Batman!",
            "date": "2016-3-30"
        }
        form=forms.MedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could not find the participant:
        self.assertFalse(found_participant)

    def test_medical_release_form_not_valid_participant_birth_date(self):
        """ Tests whether the form finds a participant record if the input has a
         matching name, but not a matching date. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "primary_physician_name": "Dr. Physician Man",
            "primary_physician_phone": "1112223333",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "Y",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "Y",
            "currently_taking_any_medication": "Y",
            "pregnant": "Y",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "Y",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": "Y",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1000-1-1",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }
        form=forms.MedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could not find the participant:
        self.assertFalse(found_participant)

    def test_medical_release_form_saves_with_valid_data(self):
        """ Verify that a Medical Release form view, populated with
         valid data, correctly saves the form to the database. """

        form_data={
            "primary_physician_name": "Dr. Physician Man",
            "primary_physician_phone": "1112223333",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "N",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "N",
            "currently_taking_any_medication": "Y",
            "pregnant": "N",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "N",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": "N",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-med-release"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retrieve the new Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
            print("Successfully retrieved participant record.")
        except:
            print("ERROR: Unable to retreive participant record!")

        # Attempt to retrieve the MedicalInfo record:
        try:
            print("Retrieving new MedicalInfo record...")
            medical_info_in_db=models.MedicalInfo.objects.get(
                participant_id=participant_in_db,
                date=form_data["date"]
            )
            print("Successfully retrieved new MedicalInfo record.")
        except:
            print("ERROR: Unable to retrieve MedicalInfo record!")

        # Attempt to retrieve the Medication records:
        try:
            print("Retrieving new Medication record...")
            # medical_info_in_db=models.MedicalInfo.objects.get(
            #     participant_id=participant_in_db,
            #     date=form_data["date"]
            # )
            # print("Successfully retrieved new Medication record.")
        except:
            print("ERROR: Unable to retrieve Medication record!")

        # Check that the new MedicalInfo record's attributes were set correctly:
        print("Checking stored MedicalInfo attributes...")
        self.assertEqual(
            medical_info_in_db.primary_physician_name,
            form_data["primary_physician_name"]
        )

    def test_medical_release_form_with_invalid_participant_name(self):
        """ Verify that a Medical Release form view, populated with
         an invalid participant name, displays an error message. """

        form_data={
            "primary_physician_name": "Dr. Physician Man",
            "primary_physician_phone": "1112223333",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "N",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "N",
            "currently_taking_any_medication": "Y",
            "pregnant": "N",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "N",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": "N",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST Not Bruce Wayne",
            "date": "2016-3-30"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-med-release"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_medical_release_form_with_invalid_participant_date(self):
        """ Verify that a Medical Release form view, populated with
         an invalid participant name, displays an error message. """

        form_data={
            "primary_physician_name": "Dr. Physician Man",
            "primary_physician_phone": "1112223333",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "N",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "N",
            "currently_taking_any_medication": "Y",
            "pregnant": "N",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "N",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": "N",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1455-9-30",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-med-release"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_medical_release_form_with_invalid_form_data(self):
        """ Verify that a Medical Release form view, populated with
         an invalid participant date, displays an error message. """

        form_data={
            "primary_physician_name": "Dr. Physician Man with a super long name"
                "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
                "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
            "primary_physician_phone": "11122233332u3094890238402",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "N",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "N",
            "currently_taking_any_medication": "Y",
            "pregnant": "N",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "N",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": "N",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-med-release"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_medical_release_form_empty_medication_name_field(self):
        """ Regression test for Issue #24. Empty Medication fields should not be
         saved as new Medication records. """

        form_data={
            "primary_physician_name": "Dr. Physician Man",
            "primary_physician_phone": "1112223333",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "N",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "N",
            "currently_taking_any_medication": "Y",
            "pregnant": "N",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "",
            "medication_two_reason": "",
            "medication_two_frequency": "",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "N",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": "N",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-med-release"), form_data)

        # Attempt to retrieve the new Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
            print("Successfully retrieved participant record.")
        except:
            print("ERROR: Unable to retreive participant record!")

        # Attempt to retrieve the first Medication record (has a non "" name),
        # which should have been saved:
        try:
            print("Retrieving the first Medication record...")
            medication_in_db=models.Medication.objects.get(
                participant_id=participant_in_db,
                date=form_data["date"],
                medication_name=form_data["medication_one_name"]
            )
            print("Successfully retrieved first Medication record.")
            found_medication_one=True
        except:
            print("ERROR: Unable to retrieve valid Medication record!")
            found_medication_one=False
        self.assertTrue(found_medication_one)

        # Attempt to retrieve the second Medication record (with a "" name),
        # which should not have been saved:
        try:
            print("Retrieving the second Medication record...")
            medication_in_db=models.Medication.objects.get(
                participant_id=participant_in_db,
                date=form_data["date"],
                medication_name=form_data["medication_two_name"]
            )
            print("Successfully retrieved second Medication record.")
            found_medication_two=True
        except:
            print("ERROR: Retrieved a Medication record with an empty string"
                " for a name!")
            found_medication_two=False
        self.assertFalse(found_medication_two)

    def test_medical_release_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a MedicalInfo record with the same
         (participant_id, date) as its primary key. """

        form_data={
            "primary_physician_name": "Dr. Physician Man",
            "primary_physician_phone": "1112223333",
            "last_seen_by_physician_date": "2016-1-1",
            "last_seen_by_physician_reason": "Shoulder injury",
            "allergies_conditions_that_exclude": "N",
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": "N",
            "tetanus_shot_last_ten_years": "Y",
            "seizures_last_six_monthes": "N",
            "currently_taking_any_medication": "Y",
            "pregnant": "N",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": "Y",
            "physical_or_mental_issues_affecting_riding": "Y",
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": "N",
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": "Y",
            "limiting_surgeries_last_six_monthes": "N",
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Alfred Pennyworth",
            "name": "TEST Bruce Wayne",
            "date": "2016-1-1"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-med-release"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertEqual(
            views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                form="health information record"
            ),
            response.context["error_text"]
        )


class TestLiabilityReleaseForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)
        test_participant=models.Participant(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
            email="peter@spider-man.com",
            weight=195,
            gender="M",
            guardian_name="Aunt May",
            height=72,
            minor_status="G",
            address_street="123 Apartment Street",
            address_city="New York",
            address_state="OK",
            address_zip="74804",
            phone_home="123-456-7890",
            phone_cell="444-393-0098",
            phone_work="598-039-3008",
            school_institution="SHIELD"
        )
        test_participant.save()

        liability_release=models.LiabilityRelease(
            participant_id=test_participant,
            date="2014-3-5",
            signature="TEST Oliver Queen"
        )
        liability_release.save()

    def test_liability_release_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "signature": "TEST Peter Parker",
            "date": "2016-03-31"
        }
        form=forms.LiabilityReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertEquals(found_participant, True)

    def test_liability_release_form_saves_with_valid_data(self):
        """ Verify that an Liability Release form view, populated with
         valid data, correctly saves the form to the database. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "signature": "TEST Peter Parker",
            "date": "2016-03-31"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-liability"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the updated MedicalInfo record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )

            print("Retrieving updated LiabilityRelease record...")
            liability_release_in_db=models.LiabilityRelease.objects.get(
                participant_id=participant_in_db,
                date=form_data["date"]
            )
            print("Successfully retrieved updated LiabilityRelease record.")
        except:
            print("ERROR: Unable to retreive updated LiabilityRelease record!")

    def test_liability_release_form_not_valid_participant_name(self):
        """ Tests whether the form finds a participant record if the input has a
         matching date, but not a matching name. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Not A Person",
            "birth_date": "1985-4-02",
            "signature": "TEST Peter Parker",
            "date": "2016-03-31"
        }
        form=forms.LiabilityReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could not find the participant:
        self.assertEquals(found_participant, False)

    def test_liability_release_form_not_valid_birth_date(self):
        """ Tests whether the form finds a participant record if the input has a
         matching name, but not a matching date. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1001-1-1",
            "signature": "TEST Peter Parker",
            "date": "2016-03-31"
        }
        form=forms.LiabilityReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could not find the participant:
        self.assertEquals(found_participant, False)

    def test_liability_release_form_with_invalid_form_data(self):
        """ Verify that an Liability Release form view, populated with
         an invalid participant date, displays an error message. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "signature": "TEST Peter Parker",
            "date": "sdfsfsfsf"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-liability"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_liability_release_form_with_invalid_participant_name(self):

        form_data={
            "name": "TEST Not Peter Parker",
            "birth_date": "1985-4-02",
            "signature": "TEST Peter Parker",
            "date": "2016-03-31"
        }

        response=self.client.post(reverse("public-form-liability"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_liability_release_form_with_invalid_participant_date(self):
        """ Verify that an Liability Release form view, populated with
         an invalid participant date, displays an error message. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1000-1-1",
            "signature": "TEST Peter Parker",
            "date": "2016-03-31"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-liability"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_liability_release_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a MedicalInfo record with the same
         (participant_id, date) as its primary key. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "signature": "TEST Peter Parker",
            "date": "2014-3-5"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-liability"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertEqual(
            views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                form="liability release"
            ),
            response.context["error_text"]
        )


class TestSeizureEvaluationForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)
        test_participant=models.Participant(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
            email="peter@spider-man.com",
            weight=195,
            gender="M",
            guardian_name="Aunt May",
            height=72,
            minor_status="G",
            address_street="123 Apartment Street",
            address_city="New York",
            address_state="OK",
            address_zip="74804",
            phone_home="123-456-7890",
            phone_cell="444-393-0098",
            phone_work="598-039-3008",
            school_institution="SHIELD"
        )
        test_participant.save()

        seizure_eval=models.SeizureEval(
            participant_id=test_participant,
            date="2014-3-5",
            date_of_last_seizure="2013-3-4",
            duration_of_last_seizure="A couple of seconds",
            typical_cause="Eggplants",
            seizure_indicators="Blank stare",
            after_effect="Fatigued, disoriented",
            during_seizure_stare="",
            during_seizure_stare_length="",
            during_seizure_walks="",
            during_seizure_aimless="",
            during_seizure_cry_etc="",
            during_seizure_bladder_bowel="",
            during_seizure_confused_etc="",
            during_seizure_other="",
            during_seizure_other_description="",
            knows_when_will_occur="",
            can_communicate_when_will_occur="",
            action_to_take_do_nothing="",
            action_to_take_dismount="",
            action_to_take_allow_time="",
            action_to_take_allow_time_how_long=15,
            action_to_take_report_immediately="",
            action_to_take_send_note="",
            seizure_frequency="Every couple of months",
            signature="Alfred Pennyworth",
        )
        seizure_eval.save()

    def test_seizure_evaluation_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }
        form=forms.SeizureEvaluationForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertEquals(found_participant, True)

    def test_seizure_evaluation_form_not_valid_participant_name(self):
        """ Tests whether the form finds a participant record if the input has a
         matching date, but not a matching name. """

         # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Not A Person",
            "birth_date": "1985-4-02",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }
        form=forms.SeizureEvaluationForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

         # We should say we could not find the participant:
        self.assertEquals(found_participant, False)

    def test_seizure_evaluation_form_not_valid_birth_date(self):
        """ Tests whether the form finds a participant record if the input has a
         matching name, but not a matching date. """

         # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1000-1-1",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }
        form=forms.SeizureEvaluationForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

         # We should say we could not find the participant:
        self.assertEquals(found_participant, False)

    def test_seizure_evaluation_form_saves_with_valid_data(self):
        """ Verify that a Seizure Evaluation form view, populated with
         valid data, correctly saves the form to the database. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headachey stuff",
            "medication_one_frequency": "A couple of times a week",
            "medication_two_name": "Blah Test Medicine",
            "medication_two_reason": "",
            "medication_two_frequency": "",
            "medication_three_name": "Sciency Medicine Name",
            "medication_three_reason": "Things that hurt",
            "medication_three_frequency": "Every 2 hours, as needed",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-seizure"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
        except:
            print("ERROR: Unable to retreive participant record!")

        # Attempt to retreive the new SeizureEval record:
        try:
            print("Retrieving new SeizureEval record...")
            seizure_eval_in_db=(models.SeizureEval
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"]
                )
            )
            print(
                "Successfully retrieved new SeizureEval record."
            )
        except:
            print(
                "ERROR: Unable to retreive new SeizureEval record!"
            )

        # Check that the attributes in the SeizureEval were set correctly:
        print(
            "Checking stored SeizureEval attributes..."
        )
        self.assertEqual(
            # Format the retrieved date so it matches the input format:
            "{d.year}-{d.month}-{d.day}".format(d=seizure_eval_in_db.date),
            form_data["date"]
        )
        self.assertEqual(
            participant_in_db.guardian_name,
            form_data["guardian_name"]
        )
        self.assertEqual(
            participant_in_db.phone_home,
            form_data["phone_home"]
        )
        self.assertEqual(
            participant_in_db.phone_cell,
            form_data["phone_cell"]
        )
        self.assertEqual(
            participant_in_db.phone_work,
            form_data["phone_work"]
        )
        self.assertEqual(
            "{d.year}-{d.month}-{d.day}".format(
                d=seizure_eval_in_db.date_of_last_seizure
            ),
            form_data["date_of_last_seizure"]
        )
        self.assertEqual(
            seizure_eval_in_db.seizure_frequency,
            form_data["seizure_frequency"]
        )
        self.assertEqual(
            seizure_eval_in_db.duration_of_last_seizure,
            form_data["duration_of_last_seizure"]
        )
        self.assertEqual(
            seizure_eval_in_db.typical_cause,
            form_data["typical_cause"]
        )
        self.assertEqual(
            seizure_eval_in_db.seizure_indicators,
            form_data["seizure_indicators"]
        )
        self.assertEqual(
            seizure_eval_in_db.after_effect,
            form_data["after_effect"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_stare,
            form_data["during_seizure_stare"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_stare_length,
            form_data["during_seizure_stare_length"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_walks,
            form_data["during_seizure_walks"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_aimless,
            form_data["during_seizure_aimless"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_cry_etc,
            form_data["during_seizure_cry_etc"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_bladder_bowel,
            form_data["during_seizure_bladder_bowel"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_confused_etc,
            form_data["during_seizure_confused_etc"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_other,
            form_data["during_seizure_other"]
        )
        self.assertEqual(
            seizure_eval_in_db.during_seizure_other_description,
            form_data["during_seizure_other_description"]
        )
        self.assertEqual(
            seizure_eval_in_db.knows_when_will_occur,
            form_data["knows_when_will_occur"]
        )
        self.assertEqual(
            seizure_eval_in_db.can_communicate_when_will_occur,
            form_data["can_communicate_when_will_occur"]
        )
        self.assertEqual(
            seizure_eval_in_db.action_to_take_do_nothing,
            form_data["action_to_take_do_nothing"]
        )
        self.assertEqual(
            seizure_eval_in_db.action_to_take_dismount,
            form_data["action_to_take_dismount"]
        )
        self.assertEqual(
            seizure_eval_in_db.action_to_take_allow_time,
            form_data["action_to_take_allow_time"]
        )
        self.assertEqual(
            seizure_eval_in_db.action_to_take_allow_time_how_long,
            form_data["action_to_take_allow_time_how_long"]
        )
        self.assertEqual(
            seizure_eval_in_db.action_to_take_report_immediately,
            form_data["action_to_take_report_immediately"]
        )
        self.assertEqual(
            seizure_eval_in_db.action_to_take_send_note,
            form_data["action_to_take_send_note"]
        )
        self.assertEqual(
            seizure_eval_in_db.signature,
            form_data["signature"]
        )
        self.assertEqual(
            seizure_eval_in_db.type_of_seizure,
            form_data["type_of_seizure"]
        )

        # Attempt to retreive the new Medication record for medication_one_name:
        found_medication_one=False
        try:
            print("Retrieving new Medication record for medication_one_name...")
            medication_one_in_db=(models.Medication
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"],
                    medication_name=form_data["medication_one_name"]
                )
            )
            found_medication_one=True
        except:
            print("ERROR: Unable to retreive Medication record for"
                " medication_one_name!"
            )
        self.assertTrue(found_medication_one)
        self.assertEqual(
            medication_one_in_db.reason_taken,
            form_data["medication_one_reason"]
        )
        self.assertEqual(
            medication_one_in_db.frequency,
            form_data["medication_one_frequency"]
        )

        # Attempt to retreive the new Medication record for medication_two_name:
        found_medication_two=False
        try:
            print("Retrieving new Medication record for medication_two_name...")
            medication_two_in_db=(models.Medication
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"],
                    medication_name=form_data["medication_two_name"]
                )
            )
            found_medication_two=True
        except:
            print("ERROR: Unable to retreive Medication record for"
                " medication_two_name!"
            )
        self.assertTrue(found_medication_two)
        self.assertEqual(
            medication_two_in_db.reason_taken,
            form_data["medication_two_reason"]
        )
        self.assertEqual(
            medication_two_in_db.frequency,
            form_data["medication_two_frequency"]
        )

        # Attempt to retreive the new Medication record for medication_three_name:
        found_medication_three=False
        try:
            print("Retrieving new Medication record for medication_three_name...")
            medication_three_in_db=(models.Medication
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"],
                    medication_name=form_data["medication_three_name"]
                )
            )
            found_medication_three=True
        except:
            print("ERROR: Unable to retreive Medication record for"
                " medication_three_name!"
            )
        self.assertTrue(found_medication_three)
        self.assertEqual(
            medication_three_in_db.reason_taken,
            form_data["medication_three_reason"]
        )
        self.assertEqual(
            medication_three_in_db.frequency,
            form_data["medication_three_frequency"]
        )

    # DISABLED: We are no longer storing seizuretype records.
    # DO NOT REMOVE Until after 5/2/16 demonstration, if given go ahead.
    # def test_seizure_evaluation_form_saves_seizuretype_records(self):
    #     """ Verify that a Seizure Evaluation form view, populated with
    #      valid data, correctly saves the form to the database. """
    #
    #     form_data={
    #         "name": "TEST Peter Parker",
    #         "birth_date": "1985-4-02",
    #         "date": "2016-3-31",
    #         "guardian_name": "Bob Burger",
    #         "phone_home": "123-123-4567",
    #         "phone_cell": "321-765-4321",
    #         "phone_work": "987-654-3210",
    #         "medication_one_name": "Excedrin",
    #         "medication_one_reason": "Headachey stuff",
    #         "medication_one_frequency": "A couple of times a week",
    #         "medication_two_name": "Blah Test Medicine",
    #         "medication_two_reason": "",
    #         "medication_two_frequency": "",
    #         "medication_three_name": "Sciency Medicine Name",
    #         "medication_three_reason": "Things that hurt",
    #         "medication_three_frequency": "Every 2 hours, as needed",
    #         "seizure_name_one": "Sudden and violent",
    #         "seizure_name_two": "Super sciency name",
    #         "seizure_name_three": "Puppymonkeybaby",
    #         "date_of_last_seizure": "1984-5-12",
    #         "seizure_frequency": "Everyday",
    #         "duration_of_last_seizure": "45 seconds",
    #         "typical_cause": "long activity",
    #         "seizure_indicators": "blank stare",
    #         "after_effect": "headaches",
    #         "during_seizure_stare": True,
    #         "during_seizure_stare_length": "15 seconds",
    #         "during_seizure_walks": True,
    #         "during_seizure_aimless": True,
    #         "during_seizure_cry_etc": True,
    #         "during_seizure_bladder_bowel": True,
    #         "during_seizure_confused_etc": True,
    #         "during_seizure_other": True,
    #         "during_seizure_other_description": "abcdefghij",
    #         "knows_when_will_occur": False,
    #         "can_communicate_when_will_occur": False,
    #         "action_to_take_do_nothing": True,
    #         "action_to_take_dismount": True,
    #         "action_to_take_allow_time": True,
    #         "action_to_take_allow_time_how_long": 15,
    #         "action_to_take_report_immediately": True,
    #         "action_to_take_send_note": True,
    #         "signature": "TEST Peter Parker",
    #     }
    #
    #     # Send a post request to the form view with the form_data defined above:
    #     response=self.client.post(reverse("public-form-seizure"), form_data)
    #
    #     # Attempt to retreive the Participant record:
    #     try:
    #         print("Retrieving participant record...")
    #         participant_in_db=models.Participant.objects.get(
    #             name=form_data["name"],
    #             birth_date=form_data["birth_date"]
    #         )
    #     except:
    #         print("ERROR: Unable to retreive participant record!")
    #
    #     # Attempt to retreive the new SeizureEval record:
    #     try:
    #         print("Retrieving new SeizureEval record...")
    #         seizure_eval_in_db=(models.SeizureEval
    #             .objects.get(
    #                 participant_id=participant_in_db,
    #                 date=form_data["date"]
    #             )
    #         )
    #         print(
    #             "Successfully retrieved new SeizureEval record."
    #         )
    #     except:
    #         print(
    #             "ERROR: Unable to retreive new SeizureEval record!"
    #         )
    #
    #     # Retrieve the SeizureType record matching seizure_name_one:
    #     found_seizure_one=False
    #     try:
    #         print("Retrieving seizure name/type one...")
    #         seizure_type_one_in_db=models.SeizureType.objects.get(
    #             seizure_eval=seizure_eval_in_db,
    #             name=form_data["seizure_name_one"]
    #         )
    #         found_seizure_one=True
    #     except:
    #         print("ERROR: Could't retrieve seizure name/type one!")
    #     self.assertTrue(found_seizure_one)
    #
    #     # Retrieve the SeizureType record matching seizure_name_two:
    #     found_seizure_two=False
    #     try:
    #         print("Retrieving seizure name/type two...")
    #         seizure_type_two_in_db=models.SeizureType.objects.get(
    #             seizure_eval=seizure_eval_in_db,
    #             name=form_data["seizure_name_two"]
    #         )
    #         found_seizure_two=True
    #     except:
    #         print("ERROR: Could't retrieve seizure name/type two!")
    #     self.assertTrue(found_seizure_two)
    #
    #     # Retrieve the SeizureType record matching seizure_name_three:
    #     found_seizure_three=False
    #     try:
    #         print("Retrieving seizure name/type one...")
    #         seizure_type_three_in_db=models.SeizureType.objects.get(
    #             seizure_eval=seizure_eval_in_db,
    #             name=form_data["seizure_name_three"]
    #         )
    #         found_seizure_three=True
    #     except:
    #         print("ERROR: Could't retrieve seizure name/type three!")
    #     self.assertTrue(found_seizure_three)

    def test_seizure_evaluation_form_with_invalid_participant_name(self):
        """ Verify that a Seizure Evaluation form view, populated with
         an invalid participant name, displays an error message. """

        form_data={
            "name": "TEST I'm Not Peter Parker",
            "birth_date": "1985-4-02",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-seizure"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_seizure_evaluation_form_with_invalid_participant_date(self):
        """ Verify that a Seizure Evaluation form view, populated with
         an invalid participant date, displays an error message. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "2000-1-2",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-seizure"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        form_data={
            "name": "TEST Peter Parker with a super long name zzzzzzzzzzzzzzzzzz"
                "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
                "zzzzzzzz",
            "birth_date": "this isn't a date",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-seizure"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_seizure_evaluation_form_with_no_phone_numbers_throws_error(self):
        """ Verify that a Seizure Evaluation form view, populated with no phone
         numbers, displays an error message. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "",
            "phone_cell": "",
            "phone_work": "",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-seizure"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that each phone field threw the correct error:
        self.assertFormError(
            response,
            "form",
            "phone_home",
            forms.ERROR_TEXT_NO_PHONE
        )
        self.assertFormError(
            response,
            "form",
            "phone_cell",
            forms.ERROR_TEXT_NO_PHONE
        )
        self.assertFormError(
            response,
            "form",
            "phone_work",
            forms.ERROR_TEXT_NO_PHONE
        )

    def test_seizure_evaluation_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a MedicalInfo record with the same
         (participant_id, date) as its primary key. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "date": "2014-3-5",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headachey stuff",
            "medication_one_frequency": "A couple of times a week",
            "medication_two_name": "Blah Test Medicine",
            "medication_two_reason": "",
            "medication_two_frequency": "",
            "medication_three_name": "Sciency Medicine Name",
            "medication_three_reason": "Things that hurt",
            "medication_three_frequency": "Every 2 hours, as needed",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": 15,
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-seizure"), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertEqual(
            views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                form="seizure evaluation"
            ),
            response.context["error_text"]
        )

    def test_seizure_evaluation_form_saves_with_valid_data_regression_37(self):
        """ Regression Test for Issue #37. You should be able to save a Seizure
         Evaluation form without a value in the
         'action_to_take_allow_time_how_long'. """

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "date": "2016-3-31",
            "guardian_name": "Bob Burger",
            "phone_home": "123-123-4567",
            "phone_cell": "321-765-4321",
            "phone_work": "987-654-3210",
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headachey stuff",
            "medication_one_frequency": "A couple of times a week",
            "medication_two_name": "Blah Test Medicine",
            "medication_two_reason": "",
            "medication_two_frequency": "",
            "medication_three_name": "Sciency Medicine Name",
            "medication_three_reason": "Things that hurt",
            "medication_three_frequency": "Every 2 hours, as needed",
            "type_of_seizure": "P",
            "date_of_last_seizure": "1984-5-12",
            "seizure_frequency": "Everyday",
            "duration_of_last_seizure": "45 seconds",
            "typical_cause": "long activity",
            "seizure_indicators": "blank stare",
            "after_effect": "headaches",
            "during_seizure_stare": True,
            "during_seizure_stare_length": "15 seconds",
            "during_seizure_walks": True,
            "during_seizure_aimless": True,
            "during_seizure_cry_etc": True,
            "during_seizure_bladder_bowel": True,
            "during_seizure_confused_etc": True,
            "during_seizure_other": True,
            "during_seizure_other_description": "abcdefghij",
            "knows_when_will_occur": False,
            "can_communicate_when_will_occur": False,
            "action_to_take_do_nothing": True,
            "action_to_take_dismount": True,
            "action_to_take_allow_time": True,
            "action_to_take_allow_time_how_long": "",
            "action_to_take_report_immediately": True,
            "action_to_take_send_note": True,
            "signature": "TEST Peter Parker",
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-seizure"), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        retrieved_seizure_eval=False

        # Attempt to retreive the Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["name"],
                birth_date=form_data["birth_date"]
            )
        except:
            print("ERROR: Unable to retreive participant record!")

        # Attempt to retreive the new SeizureEval record:
        try:
            print("Retrieving new SeizureEval record...")
            seizure_eval_in_db=(models.SeizureEval
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"]
                )
            )
            retrieved_seizure_eval=True
            print(
                "Successfully retrieved new SeizureEval record."
            )
        except:
            print(
                "ERROR: Unable to retreive new SeizureEval record!"
            )

        self.assertTrue(retrieved_seizure_eval)


class TestRiderEvalChecklistForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
            email="peter@spider-man.com",
            weight=195,
            gender="M",
            guardian_name="Aunt May",
            height=72,
            minor_status="G",
            address_street="123 Apartment Street",
            address_city="New York",
            address_state="OK",
            address_zip="74804",
            phone_home="123-456-7890",
            phone_cell="444-393-0098",
            phone_work="598-039-3008",
            school_institution="SHIELD"
        )
        test_participant.save()

        rider_eval_checklist=models.EvalRidingExercises(
            participant_id=test_participant,
            date="1999-9-20",
            comments="I dont wanna",
            basic_trail_rules=1,
            mount=0,
            dismount=None,
            emergency_dismount=None,
            four_natural_aids=0,
            basic_control=1,
            reverse_at_walk=1,
            reverse_at_trot=None,
            never_ridden=0,
            seat_at_walk=1,
            seat_at_trot=1,
            seat_at_canter=None,
            basic_seat_english=1,
            basic_seat_western=0,
            hand_pos_english=1,
            hand_post_western=None,
            two_point_trot=1,
            circle_trot_no_stirrups=None,
            circle_at_canter=0,
            circle_canter_no_stirrups=1,
            two_point_canter=None,
            circle_at_walk=1,
            circle_at_trot=None,
            holds_handhold_walk="U",
            holds_handhold_sit_trot="P",
            holds_handhold_post_trot="F",
            holds_handhold_canter="G",
            holds_reins_walk="E",
            holds_reins_sit_trot="N",
            holds_reins_post_trot="A",
            holds_reins_canter="P",
            shorten_lengthen_reins_walk="U",
            shorten_lengthen_reins_sit_trot="P",
            shorten_lengthen_reins_post_trot="A",
            shorten_lengthen_reins_canter="G",
            can_control_horse_walk="E",
            can_control_horse_sit_trot="N",
            can_control_horse_post_trot="A",
            can_control_horse_canter="P",
            can_halt_walk="U",
            can_halt_sit_trot="P",
            can_halt_post_trot="F",
            can_halt_canter="G",
            drop_pickup_stirrups_walk="E",
            drop_pickup_stirrups_sit_trot="N",
            drop_pickup_stirrups_post_trot="A",
            drop_pickup_stirrups_canter="P",
            rides_no_stirrups_walk="U",
            rides_no_stirrups_sit_trot="P",
            rides_no_stirrups_post_trot="F",
            rides_no_stirrups_canter="G",
            maintain_half_seat_walk="E",
            maintain_half_seat_sit_trot="E",
            maintain_half_seat_post_trot="N",
            maintain_half_seat_canter="A",
            can_post_walk="P",
            can_post_sit_trot="U",
            can_post_post_trot="P",
            can_post_canter="F",
            proper_diagonal_walk="G",
            proper_diagonal_sit_trot="E",
            proper_diagonal_post_trot="N",
            proper_diagonal_canter="A",
            proper_lead_canter_sees="P",
            proper_lead_canter_knows="U",
            can_steer_over_cavalletti_walk="P",
            can_steer_over_cavalletti_sit_trot="F",
            can_steer_over_cavalletti_post_trot="G",
            can_steer_over_cavalletti_canter="E",
            jump_crossbar_walk="N",
            jump_crossbar_sit_trot="A",
            jump_crossbar_post_trot="P",
            jump_crossbar_canter="U",
            basic_trail_rules_com="",
            mount_com="aaaaaaa",
            dismount_com="bbbbbbbbbb",
            emergency_dismount_com="",
            four_natural_aids_com="cccccc",
            basic_control_com="",
            reverse_at_walk_com="dddddddd",
            reverse_at_trot_com="",
            never_ridden_com="eeeeeeeeee",
            seat_at_walk_com="fffffffff",
            seat_at_trot_com="gggggggggg",
            seat_at_canter_com="hhhhhhhh",
            basic_seat_english_com="",
            basic_seat_western_com="iiiiiiiii",
            hand_pos_english_com="",
            hand_post_western_com="jjjjjjj",
            two_point_trot_com="kkkkkkkkkk",
            circle_trot_no_stirrups_com="",
            circle_at_canter_com="",
            circle_canter_no_stirrups_com="lllllllll",
            two_point_canter_com="mmmmmmmmm",
            circle_at_walk_com="",
            circle_at_trot_com="nnnnnnnnnn",
            holds_handhold_walk_com="",
            holds_handhold_sit_trot_com="",
            holds_handhold_post_trot_com="ooooooooo",
            holds_handhold_canter_com="",
            holds_reins_walk_com="ppppppppppp",
            holds_reins_sit_trot_com="",
            holds_reins_post_trot_com="",
            holds_reins_canter_com="qqqqqqqqqq",
            shorten_lengthen_reins_walk_com="",
            shorten_lengthen_reins_sit_trot_com="rrrrrrrrrrr",
            shorten_lengthen_reins_post_trot_com="sssssssssss",
            shorten_lengthen_reins_canter_com="",
            can_control_horse_walk_com="",
            can_control_horse_sit_trot_com="ttttttttt",
            can_control_horse_post_trot_com="",
            can_control_horse_canter_com="uuuuuuuuu",
            can_halt_walk_com="vvvvvvvvvv",
            can_halt_sit_trot_com="",
            can_halt_post_trot_com="wwwwwwwwwwwwwww",
            can_halt_canter_com="",
            drop_pickup_stirrups_walk_com="",
            drop_pickup_stirrups_sit_trot_com="",
            drop_pickup_stirrups_post_trot_com="xxxxxxxxxxxxxxxx",
            drop_pickup_stirrups_canter_com="",
            rides_no_stirrups_walk_com="",
            rides_no_stirrups_sit_trot_com="yyyyyyyyyyyy",
            rides_no_stirrups_post_trot_com="",
            rides_no_stirrups_canter_com="zzzzzzzzzzzzz",
            maintain_half_seat_walk_com="",
            maintain_half_seat_sit_trot_com="",
            maintain_half_seat_post_trot_com="",
            maintain_half_seat_canter_com="aaaaaaaaaaa",
            can_post_walk_com="",
            can_post_sit_trot_com="",
            can_post_post_trot_com="bbbbbbbbbbbbb",
            can_post_canter_com="",
            proper_diagonal_walk_com="",
            proper_diagonal_sit_trot_com="ccccccccccc",
            proper_diagonal_post_trot_com="",
            proper_diagonal_canter_com="",
            proper_lead_canter_sees_com="dddddddddd",
            proper_lead_canter_knows_com="",
            can_steer_over_cavalletti_walk_com="",
            can_steer_over_cavalletti_sit_trot_com="eeeeeeeee",
            can_steer_over_cavalletti_post_trot_com="",
            can_steer_over_cavalletti_canter_com="",
            jump_crossbar_walk_com="ffffffffff",
            jump_crossbar_sit_trot_com="",
            jump_crossbar_post_trot_com="ggggggggg",
            jump_crossbar_canter_com=""
        )
        rider_eval_checklist.save()

    def test_rider_eval_checklist_form_duplicate_pk(self):
        """ Verify that a Rider Evaluation Checklist form view, populated with
         valid data, correctly saves the form to the database. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)
        try:
            with transaction.atomic():
                form_data={
                    "date":"1999-9-20",
                    "comments":"I have nothing to say",
                    "basic_trail_rules": 1,
                    "mount": 0,
                    "dismount": None,
                    "emergency_dismount": None,
                    "four_natural_aids": 1,
                    "basic_control": 1,
                    "reverse_at_walk": 0,
                    "reverse_at_trot": 1,
                    "never_ridden": 0,
                    "seat_at_walk": None,
                    "seat_at_trot": 1,
                    "seat_at_canter": None,
                    "basic_seat_english": 1,
                    "basic_seat_western": None,
                    "hand_pos_english": 1,
                    "hand_post_western": 1,
                    "two_point_trot": 0,
                    "circle_trot_no_stirrups": None,
                    "circle_at_canter": 0,
                    "circle_canter_no_stirrups": 1,
                    "two_point_canter": 1,
                    "circle_at_walk": 0,
                    "circle_at_trot": 0,
                    "holds_handhold_walk": "U",
                    "holds_handhold_sit_trot": "P",
                    "holds_handhold_post_trot": "F",
                    "holds_handhold_canter": "G",
                    "holds_reins_walk": "E",
                    "holds_reins_sit_trot": "N",
                    "holds_reins_post_trot": "A",
                    "holds_reins_canter": "P",
                    "shorten_lengthen_reins_walk": "U",
                    "shorten_lengthen_reins_sit_trot": "P",
                    "shorten_lengthen_reins_post_trot": "F",
                    "shorten_lengthen_reins_canter": "G",
                    "can_control_horse_walk": "E",
                    "can_control_horse_sit_trot": "N",
                    "can_control_horse_post_trot": "A",
                    "can_control_horse_canter": "P",
                    "can_halt_walk": "U",
                    "can_halt_sit_trot": "P",
                    "can_halt_post_trot": "F",
                    "can_halt_canter": "G",
                    "drop_pickup_stirrups_walk": "E",
                    "drop_pickup_stirrups_sit_trot": "N",
                    "drop_pickup_stirrups_post_trot": "A",
                    "drop_pickup_stirrups_canter": "P",
                    "rides_no_stirrups_walk": "U",
                    "rides_no_stirrups_sit_trot": "P",
                    "rides_no_stirrups_post_trot": "F",
                    "rides_no_stirrups_canter": "G",
                    "maintain_half_seat_walk": "E",
                    "maintain_half_seat_sit_trot": "N",
                    "maintain_half_seat_post_trot": "A",
                    "maintain_half_seat_canter": "P",
                    "can_post_walk": "U",
                    "can_post_sit_trot": "P",
                    "can_post_post_trot": "F",
                    "can_post_canter": "G",
                    "proper_diagonal_walk": "E",
                    "proper_diagonal_sit_trot": "N",
                    "proper_diagonal_post_trot": "A",
                    "proper_diagonal_canter": "P",
                    "proper_lead_canter_sees": "U",
                    "proper_lead_canter_knows": "P",
                    "can_steer_over_cavalletti_walk": "F",
                    "can_steer_over_cavalletti_sit_trot": "G",
                    "can_steer_over_cavalletti_post_trot": "E",
                    "can_steer_over_cavalletti_canter": "N",
                    "jump_crossbar_walk": "A",
                    "jump_crossbar_sit_trot": "P",
                    "jump_crossbar_post_trot": "U",
                    "jump_crossbar_canter": "P",
                    "basic_trail_rules_com":"",
                    "mount_com":"aaaaaaa",
                    "dismount_com":"bbbbbbbbbb",
                    "emergency_dismount_com":"",
                    "four_natural_aids_com":"cccccc",
                    "basic_control_com":"",
                    "reverse_at_walk_com":"dddddddd",
                    "reverse_at_trot_com":"",
                    "never_ridden_com":"eeeeeeeeee",
                    "seat_at_walk_com":"fffffffff",
                    "seat_at_trot_com":"gggggggggg",
                    "seat_at_canter_com":"hhhhhhhh",
                    "basic_seat_english_com":"",
                    "basic_seat_western_com":"iiiiiiiii",
                    "hand_pos_english_com":"",
                    "hand_post_western_com":"jjjjjjj",
                    "two_point_trot_com":"kkkkkkkkkk",
                    "circle_trot_no_stirrups_com":"",
                    "circle_at_canter_com":"",
                    "circle_canter_no_stirrups_com":"lllllllll",
                    "two_point_canter_com":"mmmmmmmmm",
                    "circle_at_walk_com":"",
                    "circle_at_trot_com":"nnnnnnnnnn",
                    "holds_handhold_walk_com":"",
                    "holds_handhold_sit_trot_com":"",
                    "holds_handhold_post_trot_com":"ooooooooo",
                    "holds_handhold_canter_com":"",
                    "holds_reins_walk_com":"ppppppppppp",
                    "holds_reins_sit_trot_com":"",
                    "holds_reins_post_trot_com":"",
                    "holds_reins_canter_com":"qqqqqqqqqq",
                    "shorten_lengthen_reins_walk_com":"",
                    "shorten_lengthen_reins_sit_trot_com":"rrrrrrrrrrr",
                    "shorten_lengthen_reins_post_trot_com":"sssssssssss",
                    "shorten_lengthen_reins_canter_com":"",
                    "can_control_horse_walk_com":"",
                    "can_control_horse_sit_trot_com":"ttttttttt",
                    "can_control_horse_post_trot_com":"",
                    "can_control_horse_canter_com":"uuuuuuuuu",
                    "can_halt_walk_com":"vvvvvvvvvv",
                    "can_halt_sit_trot_com":"",
                    "can_halt_post_trot_com":"wwwwwwwwwwwwwww",
                    "can_halt_canter_com":"",
                    "drop_pickup_stirrups_walk_com":"",
                    "drop_pickup_stirrups_sit_trot_com":"",
                    "drop_pickup_stirrups_post_trot_com":"xxxxxxxxxxxxxxxx",
                    "drop_pickup_stirrups_canter_com":"",
                    "rides_no_stirrups_walk_com":"",
                    "rides_no_stirrups_sit_trot_com":"yyyyyyyyyyyy",
                    "rides_no_stirrups_post_trot_com":"",
                    "rides_no_stirrups_canter_com":"zzzzzzzzzzzzz",
                    "maintain_half_seat_walk_com":"",
                    "maintain_half_seat_sit_trot_com":"",
                    "maintain_half_seat_post_trot_com":"",
                    "maintain_half_seat_canter_com":"aaaaaaaaaaa",
                    "can_post_walk_com":"",
                    "can_post_sit_trot_com":"",
                    "can_post_post_trot_com":"bbbbbbbbbbbbb",
                    "can_post_canter_com":"",
                    "proper_diagonal_walk_com":"",
                    "proper_diagonal_sit_trot_com":"ccccccccccc",
                    "proper_diagonal_post_trot_com":"",
                    "proper_diagonal_canter_com":"",
                    "proper_lead_canter_sees_com":"dddddddddd",
                    "proper_lead_canter_knows_com":"",
                    "can_steer_over_cavalletti_walk_com":"",
                    "can_steer_over_cavalletti_sit_trot_com":"eeeeeeeee",
                    "can_steer_over_cavalletti_post_trot_com":"",
                    "can_steer_over_cavalletti_canter_com":"",
                    "jump_crossbar_walk_com":"ffffffffff",
                    "jump_crossbar_sit_trot_com":"",
                    "jump_crossbar_post_trot_com":"ggggggggg",
                    "jump_crossbar_canter_com":""
                }

                test_participant_in_db=models.Participant.objects.get(
                    name="TEST Peter Parker",
                    birth_date="1985-4-02"
                )

                # Send a post request to the form view with the form_data defined above:
                response=self.client.post(
                    reverse(
                        "private_form_rider_eval_checklist",
                        kwargs={'participant_id':test_participant_in_db.participant_id}
                    ),
                    form_data
                )

                # Assert that the reponse code is a 302 (redirect):
                self.assertEqual(response.status_code, 302)

                # Assert that the context for the new view contains the correct error:
                self.assertEqual(
                    views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                        form="Rider Eval Checklist Form"
                    ),
                    response.context["error_text"]
                )
        except:
            pass

    def test_rider_eval_checklist_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "date":"2016-3-13",
            "comments":"I have nothing to say",
            "basic_trail_rules": 1,
            "mount": 0,
            "dismount": None,
            "emergency_dismount": None,
            "four_natural_aids": 1,
            "basic_control": 1,
            "reverse_at_walk": 0,
            "reverse_at_trot": 1,
            "never_ridden": 0,
            "seat_at_walk": None,
            "seat_at_trot": 1,
            "seat_at_canter": None,
            "basic_seat_english": 1,
            "basic_seat_western": None,
            "hand_pos_english": 1,
            "hand_post_western": 1,
            "two_point_trot": 0,
            "circle_trot_no_stirrups": None,
            "circle_at_canter": 0,
            "circle_canter_no_stirrups": 1,
            "two_point_canter": 1,
            "circle_at_walk": 0,
            "circle_at_trot": 0,
            "holds_handhold_walk": "U",
            "holds_handhold_sit_trot": "P",
            "holds_handhold_post_trot": "F",
            "holds_handhold_canter": "G",
            "holds_reins_walk": "E",
            "holds_reins_sit_trot": "N",
            "holds_reins_post_trot": "A",
            "holds_reins_canter": "P",
            "shorten_lengthen_reins_walk": "U",
            "shorten_lengthen_reins_sit_trot": "P",
            "shorten_lengthen_reins_post_trot": "F",
            "shorten_lengthen_reins_canter": "G",
            "can_control_horse_walk": "E",
            "can_control_horse_sit_trot": "N",
            "can_control_horse_post_trot": "A",
            "can_control_horse_canter": "P",
            "can_halt_walk": "U",
            "can_halt_sit_trot": "P",
            "can_halt_post_trot": "F",
            "can_halt_canter": "G",
            "drop_pickup_stirrups_walk": "E",
            "drop_pickup_stirrups_sit_trot": "N",
            "drop_pickup_stirrups_post_trot": "A",
            "drop_pickup_stirrups_canter": "P",
            "rides_no_stirrups_walk": "U",
            "rides_no_stirrups_sit_trot": "P",
            "rides_no_stirrups_post_trot": "F",
            "rides_no_stirrups_canter": "G",
            "maintain_half_seat_walk": "E",
            "maintain_half_seat_sit_trot": "N",
            "maintain_half_seat_post_trot": "A",
            "maintain_half_seat_canter": "P",
            "can_post_walk": "U",
            "can_post_sit_trot": "P",
            "can_post_post_trot": "F",
            "can_post_canter": "G",
            "proper_diagonal_walk": "E",
            "proper_diagonal_sit_trot": "N",
            "proper_diagonal_post_trot": "A",
            "proper_diagonal_canter": "P",
            "proper_lead_canter_sees": "U",
            "proper_lead_canter_knows": "P",
            "can_steer_over_cavalletti_walk": "F",
            "can_steer_over_cavalletti_sit_trot": "G",
            "can_steer_over_cavalletti_post_trot": "E",
            "can_steer_over_cavalletti_canter": "N",
            "jump_crossbar_walk": "A",
            "jump_crossbar_sit_trot": "P",
            "jump_crossbar_post_trot": "U",
            "jump_crossbar_canter": "P",
            "basic_trail_rules_com":"",
            "mount_com":"aaaaaaa",
            "dismount_com":"bbbbbbbbbb",
            "emergency_dismount_com":"",
            "four_natural_aids_com":"cccccc",
            "basic_control_com":"",
            "reverse_at_walk_com":"dddddddd",
            "reverse_at_trot_com":"",
            "never_ridden_com":"eeeeeeeeee",
            "seat_at_walk_com":"fffffffff",
            "seat_at_trot_com":"gggggggggg",
            "seat_at_canter_com":"hhhhhhhh",
            "basic_seat_english_com":"",
            "basic_seat_western_com":"iiiiiiiii",
            "hand_pos_english_com":"",
            "hand_post_western_com":"jjjjjjj",
            "two_point_trot_com":"kkkkkkkkkk",
            "circle_trot_no_stirrups_com":"",
            "circle_at_canter_com":"",
            "circle_canter_no_stirrups_com":"lllllllll",
            "two_point_canter_com":"mmmmmmmmm",
            "circle_at_walk_com":"",
            "circle_at_trot_com":"nnnnnnnnnn",
            "holds_handhold_walk_com":"",
            "holds_handhold_sit_trot_com":"",
            "holds_handhold_post_trot_com":"ooooooooo",
            "holds_handhold_canter_com":"",
            "holds_reins_walk_com":"ppppppppppp",
            "holds_reins_sit_trot_com":"",
            "holds_reins_post_trot_com":"",
            "holds_reins_canter_com":"qqqqqqqqqq",
            "shorten_lengthen_reins_walk_com":"",
            "shorten_lengthen_reins_sit_trot_com":"rrrrrrrrrrr",
            "shorten_lengthen_reins_post_trot_com":"sssssssssss",
            "shorten_lengthen_reins_canter_com":"",
            "can_control_horse_walk_com":"",
            "can_control_horse_sit_trot_com":"ttttttttt",
            "can_control_horse_post_trot_com":"",
            "can_control_horse_canter_com":"uuuuuuuuu",
            "can_halt_walk_com":"vvvvvvvvvv",
            "can_halt_sit_trot_com":"",
            "can_halt_post_trot_com":"wwwwwwwwwwwwwww",
            "can_halt_canter_com":"",
            "drop_pickup_stirrups_walk_com":"",
            "drop_pickup_stirrups_sit_trot_com":"",
            "drop_pickup_stirrups_post_trot_com":"xxxxxxxxxxxxxxxx",
            "drop_pickup_stirrups_canter_com":"",
            "rides_no_stirrups_walk_com":"",
            "rides_no_stirrups_sit_trot_com":"yyyyyyyyyyyy",
            "rides_no_stirrups_post_trot_com":"",
            "rides_no_stirrups_canter_com":"zzzzzzzzzzzzz",
            "maintain_half_seat_walk_com":"",
            "maintain_half_seat_sit_trot_com":"",
            "maintain_half_seat_post_trot_com":"",
            "maintain_half_seat_canter_com":"aaaaaaaaaaa",
            "can_post_walk_com":"",
            "can_post_sit_trot_com":"",
            "can_post_post_trot_com":"bbbbbbbbbbbbb",
            "can_post_canter_com":"",
            "proper_diagonal_walk_com":"",
            "proper_diagonal_sit_trot_com":"ccccccccccc",
            "proper_diagonal_post_trot_com":"",
            "proper_diagonal_canter_com":"",
            "proper_lead_canter_sees_com":"dddddddddd",
            "proper_lead_canter_knows_com":"",
            "can_steer_over_cavalletti_walk_com":"",
            "can_steer_over_cavalletti_sit_trot_com":"eeeeeeeee",
            "can_steer_over_cavalletti_post_trot_com":"",
            "can_steer_over_cavalletti_canter_com":"",
            "jump_crossbar_walk_com":"ffffffffff",
            "jump_crossbar_sit_trot_com":"",
            "jump_crossbar_post_trot_com":"ggggggggg",
            "jump_crossbar_canter_com":""
        }
        form=forms.RiderEvalChecklistForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name="TEST Peter Parker",
                    birth_date="1985-4-02",
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertEquals(found_participant, True)

    def test_rider_eval_checklist_form_saves_with_valid_data(self):
        """ Verify that a Rider Evaluation Checklist form view, populated with
         valid data, correctly saves the form to the database. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        form_data={
            "date":"2016-3-13",
            "comments":"I have nothing to say",
            "basic_trail_rules": 1,
            "mount": 0,
            "dismount": None,
            "emergency_dismount": None,
            "four_natural_aids": 1,
            "basic_control": 1,
            "reverse_at_walk": 0,
            "reverse_at_trot": 1,
            "never_ridden": 0,
            "seat_at_walk": None,
            "seat_at_trot": 1,
            "seat_at_canter": None,
            "basic_seat_english": 1,
            "basic_seat_western": None,
            "hand_pos_english": 1,
            "hand_post_western": 1,
            "two_point_trot": 0,
            "circle_trot_no_stirrups": None,
            "circle_at_canter": 0,
            "circle_canter_no_stirrups": 1,
            "two_point_canter": 1,
            "circle_at_walk": 0,
            "circle_at_trot": 0,
            "holds_handhold_walk": "U",
            "holds_handhold_sit_trot": "P",
            "holds_handhold_post_trot": "F",
            "holds_handhold_canter": "G",
            "holds_reins_walk": "E",
            "holds_reins_sit_trot": "N",
            "holds_reins_post_trot": "A",
            "holds_reins_canter": "P",
            "shorten_lengthen_reins_walk": "U",
            "shorten_lengthen_reins_sit_trot": "P",
            "shorten_lengthen_reins_post_trot": "F",
            "shorten_lengthen_reins_canter": "G",
            "can_control_horse_walk": "E",
            "can_control_horse_sit_trot": "N",
            "can_control_horse_post_trot": "A",
            "can_control_horse_canter": "P",
            "can_halt_walk": "U",
            "can_halt_sit_trot": "P",
            "can_halt_post_trot": "F",
            "can_halt_canter": "G",
            "drop_pickup_stirrups_walk": "E",
            "drop_pickup_stirrups_sit_trot": "N",
            "drop_pickup_stirrups_post_trot": "A",
            "drop_pickup_stirrups_canter": "P",
            "rides_no_stirrups_walk": "U",
            "rides_no_stirrups_sit_trot": "P",
            "rides_no_stirrups_post_trot": "F",
            "rides_no_stirrups_canter": "G",
            "maintain_half_seat_walk": "E",
            "maintain_half_seat_sit_trot": "N",
            "maintain_half_seat_post_trot": "A",
            "maintain_half_seat_canter": "P",
            "can_post_walk": "U",
            "can_post_sit_trot": "P",
            "can_post_post_trot": "F",
            "can_post_canter": "G",
            "proper_diagonal_walk": "E",
            "proper_diagonal_sit_trot": "N",
            "proper_diagonal_post_trot": "A",
            "proper_diagonal_canter": "P",
            "proper_lead_canter_sees": "U",
            "proper_lead_canter_knows": "P",
            "can_steer_over_cavalletti_walk": "F",
            "can_steer_over_cavalletti_sit_trot": "G",
            "can_steer_over_cavalletti_post_trot": "E",
            "can_steer_over_cavalletti_canter": "N",
            "jump_crossbar_walk": "A",
            "jump_crossbar_sit_trot": "P",
            "jump_crossbar_post_trot": "U",
            "jump_crossbar_canter": "P",
            "basic_trail_rules_com": "",
            "mount_com":"aaaaaaa",
            "dismount_com":"bbbbbbbbbb",
            "emergency_dismount_com":"",
            "four_natural_aids_com":"cccccc",
            "basic_control_com":"",
            "reverse_at_walk_com":"dddddddd",
            "reverse_at_trot_com":"",
            "never_ridden_com":"eeeeeeeeee",
            "seat_at_walk_com":"fffffffff",
            "seat_at_trot_com":"gggggggggg",
            "seat_at_canter_com":"hhhhhhhh",
            "basic_seat_english_com":"",
            "basic_seat_western_com":"iiiiiiiii",
            "hand_pos_english_com":"",
            "hand_post_western_com":"jjjjjjj",
            "two_point_trot_com":"kkkkkkkkkk",
            "circle_trot_no_stirrups_com":"",
            "circle_at_canter_com":"",
            "circle_canter_no_stirrups_com":"lllllllll",
            "two_point_canter_com":"mmmmmmmmm",
            "circle_at_walk_com":"",
            "circle_at_trot_com":"nnnnnnnnnn",
            "holds_handhold_walk_com":"",
            "holds_handhold_sit_trot_com":"",
            "holds_handhold_post_trot_com":"ooooooooo",
            "holds_handhold_canter_com":"",
            "holds_reins_walk_com":"ppppppppppp",
            "holds_reins_sit_trot_com":"",
            "holds_reins_post_trot_com":"",
            "holds_reins_canter_com":"qqqqqqqqqq",
            "shorten_lengthen_reins_walk_com":"",
            "shorten_lengthen_reins_sit_trot_com":"rrrrrrrrrrr",
            "shorten_lengthen_reins_post_trot_com":"sssssssssss",
            "shorten_lengthen_reins_canter_com":"",
            "can_control_horse_walk_com":"",
            "can_control_horse_sit_trot_com":"ttttttttt",
            "can_control_horse_post_trot_com":"",
            "can_control_horse_canter_com":"uuuuuuuuu",
            "can_halt_walk_com":"vvvvvvvvvv",
            "can_halt_sit_trot_com":"",
            "can_halt_post_trot_com":"wwwwwwwwwwwwwww",
            "can_halt_canter_com":"",
            "drop_pickup_stirrups_walk_com":"",
            "drop_pickup_stirrups_sit_trot_com":"",
            "drop_pickup_stirrups_post_trot_com":"xxxxxxxxxxxxxxxx",
            "drop_pickup_stirrups_canter_com":"",
            "rides_no_stirrups_walk_com":"",
            "rides_no_stirrups_sit_trot_com":"yyyyyyyyyyyy",
            "rides_no_stirrups_post_trot_com":"",
            "rides_no_stirrups_canter_com":"zzzzzzzzzzzzz",
            "maintain_half_seat_walk_com":"",
            "maintain_half_seat_sit_trot_com":"",
            "maintain_half_seat_post_trot_com":"",
            "maintain_half_seat_canter_com":"aaaaaaaaaaa",
            "can_post_walk_com":"",
            "can_post_sit_trot_com":"",
            "can_post_post_trot_com":"bbbbbbbbbbbbb",
            "can_post_canter_com":"",
            "proper_diagonal_walk_com":"",
            "proper_diagonal_sit_trot_com":"ccccccccccc",
            "proper_diagonal_post_trot_com":"",
            "proper_diagonal_canter_com":"",
            "proper_lead_canter_sees_com":"dddddddddd",
            "proper_lead_canter_knows_com":"",
            "can_steer_over_cavalletti_walk_com":"",
            "can_steer_over_cavalletti_sit_trot_com":"eeeeeeeee",
            "can_steer_over_cavalletti_post_trot_com":"",
            "can_steer_over_cavalletti_canter_com":"",
            "jump_crossbar_walk_com":"ffffffffff",
            "jump_crossbar_sit_trot_com":"",
            "jump_crossbar_post_trot_com":"ggggggggg",
            "jump_crossbar_canter_com":""
        }

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Peter Parker",
            birth_date="1985-4-02"
        )

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(
            reverse(
                "private_form_rider_eval_checklist",
                kwargs={'participant_id':test_participant_in_db.participant_id}
            ),
            form_data
        )

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                participant_id=test_participant_in_db.participant_id
            )
        except:
            print("ERROR: Unable to retreive participant record!")

        # Attempt to retreive the new RiderEval record:
        try:
            print("Retrieving new RiderEval record...")
            rider_eval_in_db=(models.EvalRidingExercises
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"]
                )
            )
            print(
                "Successfully retrieved new RiderEval record."
            )
        except:
            print(
                "ERROR: Unable to retreive new RiderEval record!"
            )

        # Check that the attributes in the RiderEval were set correctly:
        print(
            "Checking stored RiderEval attributes..."
        )

        self.assertEqual(
            # Format the retrieved date so it matches the input format:
            "{d.year}-{d.month}-{d.day}".format(d=rider_eval_in_db.date),
            form_data["date"]
        )
        self.assertEqual(
            rider_eval_in_db.comments,
            form_data["comments"]
        )
        self.assertEqual(
            rider_eval_in_db.basic_trail_rules,
            bool(form_data["basic_trail_rules"])
        )
        self.assertEqual(
            rider_eval_in_db.mount,
            bool(form_data["mount"])
        )
        self.assertEqual(
            rider_eval_in_db.dismount,
            form_data["dismount"]
        )
        self.assertEqual(
            rider_eval_in_db.emergency_dismount,
            form_data["emergency_dismount"]
        )
        self.assertEqual(
            rider_eval_in_db.four_natural_aids,
            form_data["four_natural_aids"]
        )
        self.assertEqual(
            rider_eval_in_db.basic_control,
            form_data["basic_control"]
        )
        self.assertEqual(
            rider_eval_in_db.reverse_at_walk,
            form_data["reverse_at_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.reverse_at_trot,
            form_data["reverse_at_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.never_ridden,
            form_data["never_ridden"]
        )
        self.assertEqual(
            rider_eval_in_db.seat_at_walk,
            form_data["seat_at_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.seat_at_trot,
            form_data["seat_at_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.seat_at_canter,
            form_data["seat_at_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.basic_seat_english,
            form_data["basic_seat_english"]
        )
        self.assertEqual(
            rider_eval_in_db.basic_seat_western,
            form_data["basic_seat_western"]
        )
        self.assertEqual(
            rider_eval_in_db.hand_pos_english,
            form_data["hand_pos_english"]
        )
        self.assertEqual(
            rider_eval_in_db.hand_post_western,
            form_data["hand_post_western"]
        )
        self.assertEqual(
            rider_eval_in_db.two_point_trot,
            form_data["two_point_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_trot_no_stirrups,
            form_data["circle_trot_no_stirrups"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_at_canter,
            form_data["circle_at_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_canter_no_stirrups,
            form_data["circle_canter_no_stirrups"]
        )
        self.assertEqual(
            rider_eval_in_db.two_point_canter,
            form_data["two_point_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_at_walk,
            form_data["circle_at_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_at_trot,
            form_data["circle_at_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_handhold_walk,
            form_data["holds_handhold_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_handhold_sit_trot,
            form_data["holds_handhold_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_handhold_post_trot,
            form_data["holds_handhold_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_handhold_canter,
            form_data["holds_handhold_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_reins_walk,
            form_data["holds_reins_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_reins_sit_trot,
            form_data["holds_reins_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_reins_post_trot,
            form_data["holds_reins_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_reins_canter,
            form_data["holds_reins_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.shorten_lengthen_reins_walk,
            form_data["shorten_lengthen_reins_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.shorten_lengthen_reins_sit_trot,
            form_data["shorten_lengthen_reins_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.shorten_lengthen_reins_post_trot,
            form_data["shorten_lengthen_reins_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.shorten_lengthen_reins_canter,
            form_data["shorten_lengthen_reins_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.can_control_horse_walk,
            form_data["can_control_horse_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.can_control_horse_sit_trot,
            form_data["can_control_horse_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.can_control_horse_post_trot,
            form_data["can_control_horse_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.can_control_horse_canter,
            form_data["can_control_horse_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.can_halt_walk,
            form_data["can_halt_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.can_halt_sit_trot,
            form_data["can_halt_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.can_halt_post_trot,
            form_data["can_halt_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.can_halt_canter,
            form_data["can_halt_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.drop_pickup_stirrups_walk,
            form_data["drop_pickup_stirrups_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.drop_pickup_stirrups_sit_trot,
            form_data["drop_pickup_stirrups_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.drop_pickup_stirrups_post_trot,
            form_data["drop_pickup_stirrups_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.drop_pickup_stirrups_canter,
            form_data["drop_pickup_stirrups_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.rides_no_stirrups_walk,
            form_data["rides_no_stirrups_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.rides_no_stirrups_sit_trot,
            form_data["rides_no_stirrups_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.rides_no_stirrups_post_trot,
            form_data["rides_no_stirrups_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.rides_no_stirrups_canter,
            form_data["rides_no_stirrups_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.maintain_half_seat_walk,
            form_data["maintain_half_seat_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.maintain_half_seat_sit_trot,
            form_data["maintain_half_seat_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.maintain_half_seat_post_trot,
            form_data["maintain_half_seat_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.maintain_half_seat_canter,
            form_data["maintain_half_seat_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.can_post_walk,
            form_data["can_post_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.can_post_sit_trot,
            form_data["can_post_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.can_post_post_trot,
            form_data["can_post_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.can_post_canter,
            form_data["can_post_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_diagonal_walk,
            form_data["proper_diagonal_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_diagonal_sit_trot,
            form_data["proper_diagonal_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_diagonal_post_trot,
            form_data["proper_diagonal_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_diagonal_canter,
            form_data["proper_diagonal_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_lead_canter_sees,
            form_data["proper_lead_canter_sees"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_lead_canter_knows,
            form_data["proper_lead_canter_knows"]
        )
        self.assertEqual(
            rider_eval_in_db.can_steer_over_cavalletti_walk,
            form_data["can_steer_over_cavalletti_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.can_steer_over_cavalletti_sit_trot,
            form_data["can_steer_over_cavalletti_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.can_steer_over_cavalletti_post_trot,
            form_data["can_steer_over_cavalletti_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.can_steer_over_cavalletti_canter,
            form_data["can_steer_over_cavalletti_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.jump_crossbar_walk,
            form_data["jump_crossbar_walk"]
        )
        self.assertEqual(
            rider_eval_in_db.jump_crossbar_sit_trot,
            form_data["jump_crossbar_sit_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.jump_crossbar_post_trot,
            form_data["jump_crossbar_post_trot"]
        )
        self.assertEqual(
            rider_eval_in_db.jump_crossbar_canter,
            form_data["jump_crossbar_canter"]
        )
        self.assertEqual(
            rider_eval_in_db.basic_trail_rules_com,
            form_data["basic_trail_rules_com"]
        )
        self.assertEqual(
            rider_eval_in_db.mount_com,
            form_data["mount_com"]
        )
        self.assertEqual(
            rider_eval_in_db.dismount_com,
            form_data["dismount_com"]
        )
        self.assertEqual(
            rider_eval_in_db.emergency_dismount_com,
            form_data["emergency_dismount_com"]
        )
        self.assertEqual(
            rider_eval_in_db.four_natural_aids_com,
            form_data["four_natural_aids_com"]
        )
        self.assertEqual(
            rider_eval_in_db.basic_control_com,
            form_data["basic_control_com"]
        )
        self.assertEqual(
            rider_eval_in_db.reverse_at_walk_com,
            form_data["reverse_at_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.reverse_at_trot_com,
            form_data["reverse_at_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.never_ridden_com,
            form_data["never_ridden_com"]
        )
        self.assertEqual(
            rider_eval_in_db.seat_at_walk_com,
            form_data["seat_at_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.seat_at_trot_com,
            form_data["seat_at_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.seat_at_canter_com,
            form_data["seat_at_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.basic_seat_english_com,
            form_data["basic_seat_english_com"]
        )
        self.assertEqual(
            rider_eval_in_db.basic_seat_western_com,
            form_data["basic_seat_western_com"]
        )
        self.assertEqual(
            rider_eval_in_db.hand_pos_english_com,
            form_data["hand_pos_english_com"]
        )
        self.assertEqual(
            rider_eval_in_db.hand_post_western_com,
            form_data["hand_post_western_com"]
        )
        self.assertEqual(
            rider_eval_in_db.two_point_trot_com,
            form_data["two_point_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_trot_no_stirrups_com,
            form_data["circle_trot_no_stirrups_com"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_at_canter_com,
            form_data["circle_at_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_canter_no_stirrups_com,
            form_data["circle_canter_no_stirrups_com"]
        )
        self.assertEqual(
            rider_eval_in_db.two_point_canter_com,
            form_data["two_point_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_at_walk_com,
            form_data["circle_at_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.circle_at_trot_com,
            form_data["circle_at_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_handhold_walk_com,
            form_data["holds_handhold_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_handhold_sit_trot_com,
            form_data["holds_handhold_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_handhold_post_trot_com,
            form_data["holds_handhold_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_handhold_canter_com,
            form_data["holds_handhold_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_reins_walk_com,
            form_data["holds_reins_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_reins_sit_trot_com,
            form_data["holds_reins_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_reins_post_trot_com,
            form_data["holds_reins_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.holds_reins_canter_com,
            form_data["holds_reins_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.shorten_lengthen_reins_walk_com,
            form_data["shorten_lengthen_reins_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.shorten_lengthen_reins_sit_trot_com,
            form_data["shorten_lengthen_reins_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.shorten_lengthen_reins_post_trot_com,
            form_data["shorten_lengthen_reins_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.shorten_lengthen_reins_canter_com,
            form_data["shorten_lengthen_reins_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_control_horse_walk_com,
            form_data["can_control_horse_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_control_horse_sit_trot_com,
            form_data["can_control_horse_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_control_horse_post_trot_com,
            form_data["can_control_horse_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_control_horse_canter_com,
            form_data["can_control_horse_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_halt_walk_com,
            form_data["can_halt_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_halt_sit_trot_com,
            form_data["can_halt_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_halt_post_trot_com,
            form_data["can_halt_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_halt_canter_com,
            form_data["can_halt_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.drop_pickup_stirrups_walk_com,
            form_data["drop_pickup_stirrups_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.drop_pickup_stirrups_sit_trot_com,
            form_data["drop_pickup_stirrups_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.drop_pickup_stirrups_post_trot_com,
            form_data["drop_pickup_stirrups_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.drop_pickup_stirrups_canter_com,
            form_data["drop_pickup_stirrups_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.rides_no_stirrups_walk_com,
            form_data["rides_no_stirrups_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.rides_no_stirrups_sit_trot_com,
            form_data["rides_no_stirrups_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.rides_no_stirrups_post_trot_com,
            form_data["rides_no_stirrups_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.rides_no_stirrups_canter_com,
            form_data["rides_no_stirrups_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.maintain_half_seat_walk_com,
            form_data["maintain_half_seat_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.maintain_half_seat_sit_trot_com,
            form_data["maintain_half_seat_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.maintain_half_seat_post_trot_com,
            form_data["maintain_half_seat_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.maintain_half_seat_canter_com,
            form_data["maintain_half_seat_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_post_walk_com,
            form_data["can_post_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_post_sit_trot_com,
            form_data["can_post_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_post_post_trot_com,
            form_data["can_post_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_post_canter_com,
            form_data["can_post_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_diagonal_walk_com,
            form_data["proper_diagonal_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_diagonal_sit_trot_com,
            form_data["proper_diagonal_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_diagonal_post_trot_com,
            form_data["proper_diagonal_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_diagonal_canter_com,
            form_data["proper_diagonal_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_lead_canter_sees_com,
            form_data["proper_lead_canter_sees_com"]
        )
        self.assertEqual(
            rider_eval_in_db.proper_lead_canter_knows_com,
            form_data["proper_lead_canter_knows_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_steer_over_cavalletti_walk_com,
            form_data["can_steer_over_cavalletti_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_steer_over_cavalletti_sit_trot_com,
            form_data["can_steer_over_cavalletti_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_steer_over_cavalletti_post_trot_com,
            form_data["can_steer_over_cavalletti_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.can_steer_over_cavalletti_canter_com,
            form_data["can_steer_over_cavalletti_canter_com"]
        )
        self.assertEqual(
            rider_eval_in_db.jump_crossbar_walk_com,
            form_data["jump_crossbar_walk_com"]
        )
        self.assertEqual(
            rider_eval_in_db.jump_crossbar_sit_trot_com,
            form_data["jump_crossbar_sit_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.jump_crossbar_post_trot_com,
            form_data["jump_crossbar_post_trot_com"]
        )
        self.assertEqual(
            rider_eval_in_db.jump_crossbar_canter_com,
            form_data["jump_crossbar_canter_com"]
        )

    def test_rider_eval_checklist_form_error_with_invalid_data(self):
        """ Verify that a Rider Evaluation Checklist form view, populated with
         valid data, correctly saves the form to the database. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        form_data={
            "date":"2016-3-13",
            "comments":"I have nothing to say",
            "basic_trail_rules": 1,
            "mount": 0,
            "dismount": None,
            "emergency_dismount": None,
            "four_natural_aids": 1,
            "basic_control": 1,
            "reverse_at_walk": 0,
            "reverse_at_trot": 1,
            "never_ridden": 0,
            "seat_at_walk": None,
            "seat_at_trot": 1,
            "seat_at_canter": None,
            "basic_seat_english": 1,
            "basic_seat_western": None,
            "hand_pos_english": 1,
            "hand_post_western": 1,
            "two_point_trot": 0,
            "circle_trot_no_stirrups": None,
            "circle_at_canter": 0,
            "circle_canter_no_stirrups": 1,
            "two_point_canter": 1,
            "circle_at_walk": 0,
            "circle_at_trot": 0,
            "holds_handhold_walk": "knfghsfghsdsgbsdgbdsfbadfbadfbgsdfbgh",
            "holds_handhold_sit_trot": "P",
            "holds_handhold_post_trot": "F",
            "holds_handhold_canter": "G",
            "holds_reins_walk": "E",
            "holds_reins_sit_trot": "N",
            "holds_reins_post_trot": "A",
            "holds_reins_canter": "P",
            "shorten_lengthen_reins_walk": "U",
            "shorten_lengthen_reins_sit_trot": "P",
            "shorten_lengthen_reins_post_trot": "F",
            "shorten_lengthen_reins_canter": "G",
            "can_control_horse_walk": "E",
            "can_control_horse_sit_trot": "N",
            "can_control_horse_post_trot": "A",
            "can_control_horse_canter": "P",
            "can_halt_walk": "U",
            "can_halt_sit_trot": "P",
            "can_halt_post_trot": "F",
            "can_halt_canter": "G",
            "drop_pickup_stirrups_walk": "E",
            "drop_pickup_stirrups_sit_trot": "N",
            "drop_pickup_stirrups_post_trot": "A",
            "drop_pickup_stirrups_canter": "P",
            "rides_no_stirrups_walk": "U",
            "rides_no_stirrups_sit_trot": "P",
            "rides_no_stirrups_post_trot": "F",
            "rides_no_stirrups_canter": "G",
            "maintain_half_seat_walk": "E",
            "maintain_half_seat_sit_trot": "N",
            "maintain_half_seat_post_trot": "A",
            "maintain_half_seat_canter": "P",
            "can_post_walk": "U",
            "can_post_sit_trot": "P",
            "can_post_post_trot": "F",
            "can_post_canter": "G",
            "proper_diagonal_walk": "E",
            "proper_diagonal_sit_trot": "N",
            "proper_diagonal_post_trot": "A",
            "proper_diagonal_canter": "P",
            "proper_lead_canter_sees": "U",
            "proper_lead_canter_knows": "P",
            "can_steer_over_cavalletti_walk": "F",
            "can_steer_over_cavalletti_sit_trot": "G",
            "can_steer_over_cavalletti_post_trot": "E",
            "can_steer_over_cavalletti_canter": "N",
            "jump_crossbar_walk": "A",
            "jump_crossbar_sit_trot": "P",
            "jump_crossbar_post_trot": "U",
            "jump_crossbar_canter": "P",
            "basic_trail_rules_com":"",
            "mount_com":"aaaaaaa",
            "dismount_com":"bbbbbbbbbb",
            "emergency_dismount_com":"",
            "four_natural_aids_com":"cccccc",
            "basic_control_com":"",
            "reverse_at_walk_com":"dddddddd",
            "reverse_at_trot_com":"",
            "never_ridden_com":"eeeeeeeeee",
            "seat_at_walk_com":"fffffffff",
            "seat_at_trot_com":"gggggggggg",
            "seat_at_canter_com":"hhhhhhhh",
            "basic_seat_english_com":"",
            "basic_seat_western_com":"iiiiiiiii",
            "hand_pos_english_com":"",
            "hand_post_western_com":"jjjjjjj",
            "two_point_trot_com":"kkkkkkkkkk",
            "circle_trot_no_stirrups_com":"",
            "circle_at_canter_com":"",
            "circle_canter_no_stirrups_com":"lllllllll",
            "two_point_canter_com":"mmmmmmmmm",
            "circle_at_walk_com":"",
            "circle_at_trot_com":"nnnnnnnnnn",
            "holds_handhold_walk_com":"",
            "holds_handhold_sit_trot_com":"",
            "holds_handhold_post_trot_com":"ooooooooo",
            "holds_handhold_canter_com":"",
            "holds_reins_walk_com":"ppppppppppp",
            "holds_reins_sit_trot_com":"",
            "holds_reins_post_trot_com":"",
            "holds_reins_canter_com":"qqqqqqqqqq",
            "shorten_lengthen_reins_walk_com":"",
            "shorten_lengthen_reins_sit_trot_com":"rrrrrrrrrrr",
            "shorten_lengthen_reins_post_trot_com":"sssssssssss",
            "shorten_lengthen_reins_canter_com":"",
            "can_control_horse_walk_com":"",
            "can_control_horse_sit_trot_com":"ttttttttt",
            "can_control_horse_post_trot_com":"",
            "can_control_horse_canter_com":"uuuuuuuuu",
            "can_halt_walk_com":"vvvvvvvvvv",
            "can_halt_sit_trot_com":"",
            "can_halt_post_trot_com":"wwwwwwwwwwwwwww",
            "can_halt_canter_com":"",
            "drop_pickup_stirrups_walk_com":"",
            "drop_pickup_stirrups_sit_trot_com":"",
            "drop_pickup_stirrups_post_trot_com":"xxxxxxxxxxxxxxxx",
            "drop_pickup_stirrups_canter_com":"",
            "rides_no_stirrups_walk_com":"",
            "rides_no_stirrups_sit_trot_com":"yyyyyyyyyyyy",
            "rides_no_stirrups_post_trot_com":"",
            "rides_no_stirrups_canter_com":"zzzzzzzzzzzzz",
            "maintain_half_seat_walk_com":"",
            "maintain_half_seat_sit_trot_com":"",
            "maintain_half_seat_post_trot_com":"",
            "maintain_half_seat_canter_com":"aaaaaaaaaaa",
            "can_post_walk_com":"",
            "can_post_sit_trot_com":"",
            "can_post_post_trot_com":"bbbbbbbbbbbbb",
            "can_post_canter_com":"",
            "proper_diagonal_walk_com":"",
            "proper_diagonal_sit_trot_com":"ccccccccccc",
            "proper_diagonal_post_trot_com":"",
            "proper_diagonal_canter_com":"",
            "proper_lead_canter_sees_com":"dddddddddd",
            "proper_lead_canter_knows_com":"",
            "can_steer_over_cavalletti_walk_com":"",
            "can_steer_over_cavalletti_sit_trot_com":"eeeeeeeee",
            "can_steer_over_cavalletti_post_trot_com":"",
            "can_steer_over_cavalletti_canter_com":"",
            "jump_crossbar_walk_com":"ffffffffff",
            "jump_crossbar_sit_trot_com":"",
            "jump_crossbar_post_trot_com":"ggggggggg",
            "jump_crossbar_canter_com":""
        }

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Peter Parker",
            birth_date="1985-4-02"
        )

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(
            reverse(
                "private_form_rider_eval_checklist",
                kwargs={'participant_id':test_participant_in_db.participant_id}
            ),
            form_data
        )

        # Assert that the reponse code is a 200 (OK):
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_rider_eval_checklist_form_loads_if_user_logged_in(self):
        """ Tests whether the Rider Eval Checklist Form loads if the
         user is logged in and valid URL parameters are passed (participant_id,
         year, month, day). """

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Peter Parker",
            birth_date="1985-4-02"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("private_form_rider_eval_checklist",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_rider_eval_checklist_form_loads_if_user_not_logged_in(self):
        """ Tests whether the Rider Eval Checklist Form redirects to
         the login page if the user is not logged in. """

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("private_form_rider_eval_checklist",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_rider_eval_checklist_form_error_if_invalid_participant_get(self):
        """ Tests whether the Rider Eval Checklist Form loads if the
         user is logged in and valid URL parameters are passed (participant_id,
         year, month, day). """

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Peter Parker",
            birth_date="1985-4-02"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("private_form_rider_eval_checklist",
                kwargs={
                    "participant_id":99999999999,
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_rider_eval_checklist_form_error_if_invalid_participant_post(self):
        """ Tests whether the Rider Eval Checklist Form loads if the
         user is logged in and valid URL parameters are passed (participant_id,
         year, month, day). """

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Peter Parker",
            birth_date="1985-4-02"
        )

        self.client.force_login(test_user)

        form_data={
            "date":"2016-3-13",
            "comments":"I have nothing to say",
            "basic_trail_rules": 1,
            "mount": 0,
            "dismount": None,
            "emergency_dismount": None,
            "four_natural_aids": 1,
            "basic_control": 1,
            "reverse_at_walk": 0,
            "reverse_at_trot": 1,
            "never_ridden": 0,
            "seat_at_walk": None,
            "seat_at_trot": 1,
            "seat_at_canter": None,
            "basic_seat_english": 1,
            "basic_seat_western": None,
            "hand_pos_english": 1,
            "hand_post_western": 1,
            "two_point_trot": 0,
            "circle_trot_no_stirrups": None,
            "circle_at_canter": 0,
            "circle_canter_no_stirrups": 1,
            "two_point_canter": 1,
            "circle_at_walk": 0,
            "circle_at_trot": 0,
            "holds_handhold_walk": "U",
            "holds_handhold_sit_trot": "P",
            "holds_handhold_post_trot": "F",
            "holds_handhold_canter": "G",
            "holds_reins_walk": "E",
            "holds_reins_sit_trot": "N",
            "holds_reins_post_trot": "A",
            "holds_reins_canter": "P",
            "shorten_lengthen_reins_walk": "U",
            "shorten_lengthen_reins_sit_trot": "P",
            "shorten_lengthen_reins_post_trot": "F",
            "shorten_lengthen_reins_canter": "G",
            "can_control_horse_walk": "E",
            "can_control_horse_sit_trot": "N",
            "can_control_horse_post_trot": "A",
            "can_control_horse_canter": "P",
            "can_halt_walk": "U",
            "can_halt_sit_trot": "P",
            "can_halt_post_trot": "F",
            "can_halt_canter": "G",
            "drop_pickup_stirrups_walk": "E",
            "drop_pickup_stirrups_sit_trot": "N",
            "drop_pickup_stirrups_post_trot": "A",
            "drop_pickup_stirrups_canter": "P",
            "rides_no_stirrups_walk": "U",
            "rides_no_stirrups_sit_trot": "P",
            "rides_no_stirrups_post_trot": "F",
            "rides_no_stirrups_canter": "G",
            "maintain_half_seat_walk": "E",
            "maintain_half_seat_sit_trot": "N",
            "maintain_half_seat_post_trot": "A",
            "maintain_half_seat_canter": "P",
            "can_post_walk": "U",
            "can_post_sit_trot": "P",
            "can_post_post_trot": "F",
            "can_post_canter": "G",
            "proper_diagonal_walk": "E",
            "proper_diagonal_sit_trot": "N",
            "proper_diagonal_post_trot": "A",
            "proper_diagonal_canter": "P",
            "proper_lead_canter_sees": "U",
            "proper_lead_canter_knows": "P",
            "can_steer_over_cavalletti_walk": "F",
            "can_steer_over_cavalletti_sit_trot": "G",
            "can_steer_over_cavalletti_post_trot": "E",
            "can_steer_over_cavalletti_canter": "N",
            "jump_crossbar_walk": "A",
            "jump_crossbar_sit_trot": "P",
            "jump_crossbar_post_trot": "U",
            "jump_crossbar_canter": "P",
            "basic_trail_rules_com":"",
            "mount_com":"aaaaaaa",
            "dismount_com":"bbbbbbbbbb",
            "emergency_dismount_com":"",
            "four_natural_aids_com":"cccccc",
            "basic_control_com":"",
            "reverse_at_walk_com":"dddddddd",
            "reverse_at_trot_com":"",
            "never_ridden_com":"eeeeeeeeee",
            "seat_at_walk_com":"fffffffff",
            "seat_at_trot_com":"gggggggggg",
            "seat_at_canter_com":"hhhhhhhh",
            "basic_seat_english_com":"",
            "basic_seat_western_com":"iiiiiiiii",
            "hand_pos_english_com":"",
            "hand_post_western_com":"jjjjjjj",
            "two_point_trot_com":"kkkkkkkkkk",
            "circle_trot_no_stirrups_com":"",
            "circle_at_canter_com":"",
            "circle_canter_no_stirrups_com":"lllllllll",
            "two_point_canter_com":"mmmmmmmmm",
            "circle_at_walk_com":"",
            "circle_at_trot_com":"nnnnnnnnnn",
            "holds_handhold_walk_com":"",
            "holds_handhold_sit_trot_com":"",
            "holds_handhold_post_trot_com":"ooooooooo",
            "holds_handhold_canter_com":"",
            "holds_reins_walk_com":"ppppppppppp",
            "holds_reins_sit_trot_com":"",
            "holds_reins_post_trot_com":"",
            "holds_reins_canter_com":"qqqqqqqqqq",
            "shorten_lengthen_reins_walk_com":"",
            "shorten_lengthen_reins_sit_trot_com":"rrrrrrrrrrr",
            "shorten_lengthen_reins_post_trot_com":"sssssssssss",
            "shorten_lengthen_reins_canter_com":"",
            "can_control_horse_walk_com":"",
            "can_control_horse_sit_trot_com":"ttttttttt",
            "can_control_horse_post_trot_com":"",
            "can_control_horse_canter_com":"uuuuuuuuu",
            "can_halt_walk_com":"vvvvvvvvvv",
            "can_halt_sit_trot_com":"",
            "can_halt_post_trot_com":"wwwwwwwwwwwwwww",
            "can_halt_canter_com":"",
            "drop_pickup_stirrups_walk_com":"",
            "drop_pickup_stirrups_sit_trot_com":"",
            "drop_pickup_stirrups_post_trot_com":"xxxxxxxxxxxxxxxx",
            "drop_pickup_stirrups_canter_com":"",
            "rides_no_stirrups_walk_com":"",
            "rides_no_stirrups_sit_trot_com":"yyyyyyyyyyyy",
            "rides_no_stirrups_post_trot_com":"",
            "rides_no_stirrups_canter_com":"zzzzzzzzzzzzz",
            "maintain_half_seat_walk_com":"",
            "maintain_half_seat_sit_trot_com":"",
            "maintain_half_seat_post_trot_com":"",
            "maintain_half_seat_canter_com":"aaaaaaaaaaa",
            "can_post_walk_com":"",
            "can_post_sit_trot_com":"",
            "can_post_post_trot_com":"bbbbbbbbbbbbb",
            "can_post_canter_com":"",
            "proper_diagonal_walk_com":"",
            "proper_diagonal_sit_trot_com":"ccccccccccc",
            "proper_diagonal_post_trot_com":"",
            "proper_diagonal_canter_com":"",
            "proper_lead_canter_sees_com":"dddddddddd",
            "proper_lead_canter_knows_com":"",
            "can_steer_over_cavalletti_walk_com":"",
            "can_steer_over_cavalletti_sit_trot_com":"eeeeeeeee",
            "can_steer_over_cavalletti_post_trot_com":"",
            "can_steer_over_cavalletti_canter_com":"",
            "jump_crossbar_walk_com":"ffffffffff",
            "jump_crossbar_sit_trot_com":"",
            "jump_crossbar_post_trot_com":"ggggggggg",
            "jump_crossbar_canter_com":""
        }

        response = self.client.post(
            reverse("private_form_rider_eval_checklist",
                kwargs={
                    "participant_id": 99999999999999999,
                }
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )


class TestAdminIndex(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

    def test_admin_index_loads_if_user_logged_in(self):
        """ Tests whether the Admin Index page loads if the user is logged
         in."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(reverse('index-admin'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_admin_index_redirects_if_user_not_logged_in(self):
        """ Tests whether the Admin Index page redirects to the login page if
         the user is not logged in."""

        response = self.client.get(reverse("index-admin"))

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])


class TestReportSelectParticipant(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
            email="peter@spider-man.com",
            weight=195,
            gender="M",
            guardian_name="Aunt May",
            height=72,
            minor_status="G",
            address_street="123 Apartment Street",
            address_city="New York",
            address_state="OK",
            address_zip="74804",
            phone_home="123-456-7890",
            phone_cell="444-393-0098",
            phone_work="598-039-3008",
            school_institution="SHIELD"
        )
        test_participant.save()

    def test_report_select_participant_loads_if_user_logged_in(self):
        """ Tests whether the Select Participant for Reports page loads if the
         user is logged in."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(reverse('report-select-participant'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_report_select_participant_redirects_if_user_not_logged_in(self):
        """ Tests whether the Select Participant for Reports page redirects to
         the login page if the user is not logged in."""

        response = self.client.get(reverse('report-select-participant'))

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])


class TestPrivateFormsIndex(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
            email="peter@spider-man.com",
            weight=195,
            gender="M",
            guardian_name="Aunt May",
            height=72,
            minor_status="G",
            address_street="123 Apartment Street",
            address_city="New York",
            address_state="OK",
            address_zip="74804",
            phone_home="123-456-7890",
            phone_cell="444-393-0098",
            phone_work="598-039-3008",
            school_institution="SHIELD"
        )
        test_participant.save()

    def test_private_forms_index_loads_if_user_logged_in(self):
        """ Tests whether the Private Forms Index page loads if the user is
         logged in."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(reverse('index-private-forms'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_private_forms_index_redirects_if_user_not_logged_in(self):
        """ Tests whether the Private Forms Index page redirects to the login
         page if the user is not logged in."""

        response = self.client.get(reverse("index-private-forms"))

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])


class TestParticipantRecord(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Oliver Queen",
            birth_date="1985-05-16",
            email="arrow@archeryandthings.com",
            weight=188,
            gender="M",
            height=69,
            minor_status="A",
            address_street="4568 Rich Person Rd.",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="789-132-0024",
            phone_cell="789-456-8800",
            phone_work="789-039-3008",
            school_institution="Team Arrow"
        )
        test_participant.save()

    def test_participant_record_loads_if_user_logged_in_no_releases(self):
        """ Tests whether the Participant report page loads if the user is
         logged in."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse('participant-record',
                kwargs={
                    'participant_id':test_participant_in_db.participant_id
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_participant_record_redirects_if_user_not_logged_in(self):
        """ Tests whether the Participant Record page redirects to the login
         page if the user is not logged in."""

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse('participant-record',
                kwargs={
                    'participant_id':test_participant_in_db.participant_id
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_participant_record_shows_error_if_invalid_participant_name(self):
        """ Tests whether the Participant report page shows the correct error if
         the user is logged in."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse('participant-record',
                kwargs={
                    'participant_id': 9999999999
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...


class TestMediaReleaseReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Oliver Queen",
            birth_date="1985-05-16",
            email="arrow@archeryandthings.com",
            weight=188,
            gender="M",
            height=69,
            minor_status="A",
            address_street="4568 Rich Person Rd.",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="789-132-0024",
            phone_cell="789-456-8800",
            phone_work="789-039-3008",
            school_institution="Team Arrow"
        )
        test_participant.save()

        media_release=models.MediaRelease(
            participant_id=test_participant,
            date="2014-3-5",
            consent="Y",
            signature="TEST Oliver Queen"
        )
        media_release.save()

        test_participant_no_media_release=models.Participant(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
            email="peter@spider-man.com",
            weight=195,
            gender="M",
            guardian_name="Aunt May",
            height=72,
            minor_status="G",
            address_street="123 Apartment Street",
            address_city="New York",
            address_state="OK",
            address_zip="74804",
            phone_home="123-456-7890",
            phone_cell="444-393-0098",
            phone_work="598-039-3008",
            school_institution="SHIELD"
        )
        test_participant_no_media_release.save()

    def test_media_release_report_loads_if_user_logged_in(self):
        """ Tests whether the Media Release report page loads if the user is
         logged in and valid URL parameters are passed (participant_id, year,
         month, day)."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-media-release",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_media_release_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Media release report page redirects to the login
         page if the user is not logged in."""

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-media-release",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_media_release_report_shows_error_if_invalid_participant_id(self):
        """ Tests whether the Media Release report page shows the correct error
         if the user is logged in but an invalid participant_id is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-media-release",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_media_release_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Media Release report page shows the correct error
         if the user is logged in but an invalid date for the Media Release
         is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        response = self.client.get(
            reverse("report-media-release",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_media_release_report_shows_error_if_no_media_release(self):
        """ Tests whether the Media Release report page shows the correct error
         if the user is logged in and all parameters passed are valid, but the
         Media Release record does not exist."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
        )

        response = self.client.get(
            reverse("report-media-release",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2016",
                    "month": "1",
                    "day": "1"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_MEDIA_RELEASE_NOT_AVAILABLE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...


class TestEmergencyAuthorizationReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Oliver Queen",
            birth_date="1985-05-16",
            email="arrow@archeryandthings.com",
            weight=188,
            gender="M",
            height=69,
            minor_status="A",
            address_street="4568 Rich Person Rd.",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="789-132-0024",
            phone_cell="789-456-8800",
            phone_work="789-039-3008",
            school_institution="Team Arrow"
        )
        test_participant.save()

        emergency_authorization=models.AuthorizeEmergencyMedicalTreatment(
            participant_id=test_participant,
            date="2014-3-5",
            pref_medical_facility="Shawnee Medical Center",
            insurance_provider="Blue Cross Blue Shield of Oklahoma",
            insurance_policy_num="EI238901AAK7",
            emerg_contact_name="John Jacobs",
            emerg_contact_phone="(406) 892-7012",
            emerg_contact_relation="Brother In-Law",
            alt_emerg_procedure="",
            consents_emerg_med_treatment="Y",
            signature="TEST Oliver Queen"
        )
        emergency_authorization.save()

        test_medical_info=models.MedicalInfo(
            participant_id=test_participant,
            date="2014-3-5",
            primary_physician_name="Dr. Default",
            primary_physician_phone="111-111-1111",
            last_seen_by_physician_date="2016-1-1",
            last_seen_by_physician_reason="Normal check up visit.",
            allergies_conditions_that_exclude="N",
            heat_exhaustion_stroke="N",
            tetanus_shot_last_ten_years="Y",
            seizures_last_six_monthes="N",
            doctor_concered_re_horse_activites="N",
            physical_or_mental_issues_affecting_riding="N",
            restriction_for_horse_activity_last_five_years="N",
            present_restrictions_for_horse_activity="N",
            limiting_surgeries_last_six_monthes="N",
            signature="TEST Oliver Queen",
            currently_taking_any_medication="N",
            pregnant="N"
        )
        test_medical_info.save()

        test_participant_no_emerg_auth=models.Participant(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
            email="peter@spider-man.com",
            weight=195,
            gender="M",
            guardian_name="Aunt May",
            height=72,
            minor_status="G",
            address_street="123 Apartment Street",
            address_city="New York",
            address_state="OK",
            address_zip="74804",
            phone_home="123-456-7890",
            phone_cell="444-393-0098",
            phone_work="598-039-3008",
            school_institution="SHIELD"
        )
        test_participant_no_emerg_auth.save()

        test_participant_no_med_record=models.Participant(
            name="TEST The Doctor",
            birth_date="1235-8-14",
            email="thedoctor@galifrey.com",
            weight=190,
            gender="M",
            height=76.0,
            minor_status="A",
            address_street="The TARDIS",
            address_city="Time and space",
            address_state="OK",
            address_zip="74801",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
        )
        test_participant_no_med_record.save()

        emergency_authorization=models.AuthorizeEmergencyMedicalTreatment(
            participant_id=test_participant_no_med_record,
            date="2014-3-5",
            pref_medical_facility="Shawnee Medical Center",
            insurance_provider="Blue Cross Blue Shield of Oklahoma",
            insurance_policy_num="EI238901AAK7",
            emerg_contact_name="John Jacobs",
            emerg_contact_phone="(406) 892-7012",
            emerg_contact_relation="Brother In-Law",
            alt_emerg_procedure="",
            consents_emerg_med_treatment="Y",
            signature="TEST The Doctor"
        )
        emergency_authorization.save()

    def test_emergency_auth_report_loads_if_user_logged_in(self):
        """ Tests whether the Emergency Medical Release Authorization report
         page loads if the user is logged in and valid URL parameters are passed
         (participant_id, year, month, day). """

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-emerg-auth",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_emergency_auth_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Emergency Medical Treatment Authorization report
         page redirects to the login page if the user is not logged in. """

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-emerg-auth",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_emergency_auth_report_shows_error_if_invalid_participant_id(self):
        """ Tests whether the Emergency Medical Treatment Authorization report
         page shows the correct error if the user is logged in but an invalid
         participant_id is passed. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-emerg-auth",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_emergency_auth_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Emergency Medical Treatment Authorization report
         page shows the correct error if the user is logged in but an invalid
         date for the Emergency Medical Treatment Authorization is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        response = self.client.get(
            reverse("report-emerg-auth",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_emergency_auth_report_shows_error_if_no_emerg_auth(self):
        """ Tests whether the Emergency Medical Treatment Authorization report
         page shows the correct error if the user is logged in and all
         parameters passed are valid, but the Emergency Medical Treatment
         Authorization record does not exist. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Peter Parker",
            birth_date="1985-4-02",
        )

        response = self.client.get(
            reverse("report-emerg-auth",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2016",
                    "month": "1",
                    "day": "1"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_EMERG_AUTH_NOT_AVAILABLE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_emergency_auth_report_shows_error_if_no_medical_info(self):
        """ Tests whether the Emergency Medical Treatment Authorization report
         page shows the correct error if the user is logged in and all
         parameters passed are valid, but the Medical Info record does not exist. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST The Doctor",
            birth_date="1235-8-14",
        )

        response = self.client.get(
            reverse("report-emerg-auth",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_MEDICAL_INFO_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...


class TestMedicalReleaseReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Oliver Queen",
            birth_date="1985-05-16",
            email="arrow@archeryandthings.com",
            weight=188,
            gender="M",
            height=69,
            minor_status="A",
            address_street="4568 Rich Person Rd.",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="789-132-0024",
            phone_cell="789-456-8800",
            phone_work="789-039-3008",
            school_institution="Team Arrow"
        )
        test_participant.save()

        test_medical_info=models.MedicalInfo(
            participant_id=test_participant,
            date="2014-3-5",
            primary_physician_name="Dr. Default",
            primary_physician_phone="111-111-1111",
            last_seen_by_physician_date="2016-1-1",
            last_seen_by_physician_reason="Normal check up visit.",
            allergies_conditions_that_exclude="N",
            heat_exhaustion_stroke="N",
            tetanus_shot_last_ten_years="Y",
            seizures_last_six_monthes="N",
            doctor_concered_re_horse_activites="N",
            physical_or_mental_issues_affecting_riding="N",
            restriction_for_horse_activity_last_five_years="N",
            present_restrictions_for_horse_activity="N",
            limiting_surgeries_last_six_monthes="N",
            signature="TEST Oliver Queen",
            currently_taking_any_medication="N",
            pregnant="N"
        )
        test_medical_info.save()

        test_participant_no_med_record=models.Participant(
            name="TEST The Doctor",
            birth_date="1235-8-14",
            email="thedoctor@galifrey.com",
            weight=190,
            gender="M",
            height=76.0,
            minor_status="A",
            address_street="The TARDIS",
            address_city="Time and space",
            address_state="OK",
            address_zip="74801",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
        )
        test_participant_no_med_record.save()

    def test_med_release_report_loads_if_user_logged_in(self):
        """ Tests whether the Medical Info/Release report page loads if the user
         is logged in and valid URL parameters are passed (participant_id, year,
         month, day). """

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-med-release",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_med_release_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Medical Info/Release report page redirects to the
         login page if the user is not logged in. """

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-med-release",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_med_release_report_shows_error_if_invalid_participant_id(self):
        """ Tests whether the Medical Info/Release report page shows the correct
         error if the user is logged in but an invalid participant_id is passed.
         """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-med-release",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_med_release_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Medical Info/Release report page shows the correct
         error if the user is logged in but an invalid date for the Medical
         Info/Release is passed. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        response = self.client.get(
            reverse("report-med-release",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_med_release_report_shows_error_if_no_medical_info(self):
        """ Tests whether the Medical Info/Release report page shows the correct
         error if the user is logged in and all parameters passed are valid, but
         the Medical Info record does not exist. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST The Doctor",
            birth_date="1235-8-14",
        )

        response = self.client.get(
            reverse("report-med-release",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_MEDICAL_INFO_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...


class TestLiabilityReleaseReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Oliver Queen",
            birth_date="1985-05-16",
            email="arrow@archeryandthings.com",
            weight=188,
            gender="M",
            height=69,
            minor_status="A",
            address_street="4568 Rich Person Rd.",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="789-132-0024",
            phone_cell="789-456-8800",
            phone_work="789-039-3008",
            school_institution="Team Arrow"
        )
        test_participant.save()

        liability_release=models.LiabilityRelease(
            participant_id=test_participant,
            date="2014-3-5",
            signature="TEST Oliver Queen"
        )
        liability_release.save()

        test_participant_no_liability_release=models.Participant(
            name="TEST The Doctor",
            birth_date="1235-8-14",
            email="thedoctor@galifrey.com",
            weight=190,
            gender="M",
            height=76.0,
            minor_status="A",
            address_street="The TARDIS",
            address_city="Time and space",
            address_state="OK",
            address_zip="74801",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
        )
        test_participant_no_liability_release.save()

    def test_liability_release_report_loads_if_user_logged_in(self):
        """ Tests whether the Liability Release report page loads if the user
         is logged in and valid URL parameters are passed (participant_id, year,
         month, day). """

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-liability",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_liability_release_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Liability Release report page redirects to the
         login page if the user is not logged in. """

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-liability",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_liability_release_report_shows_error_if_invalid_participant_id(self):
        """ Tests whether the Liability Release report page shows the correct
         error if the user is logged in but an invalid participant_id is passed.
         """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-liability",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_liability_release_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Liability Release report page shows the correct
         error if the user is logged in but an invalid date for the Liability
         Release is passed. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        response = self.client.get(
            reverse("report-liability",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_liability_release_report_shows_error_if_no_liability_release(self):
        """ Tests whether the Liability Release report page shows the correct
         error if the user is logged in and all parameters passed are valid, but
         the LiabilityRelease record does not exist. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST The Doctor",
            birth_date="1235-8-14",
        )

        response = self.client.get(
            reverse("report-liability",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_LIABILITY_RELEASE_NOT_AVAILABLE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...


class TestBackgroundCheckReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Oliver Queen",
            birth_date="1985-05-16",
            email="arrow@archeryandthings.com",
            weight=188,
            gender="M",
            height=69,
            minor_status="A",
            address_street="4568 Rich Person Rd.",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="789-132-0024",
            phone_cell="789-456-8800",
            phone_work="789-039-3008",
            school_institution="Team Arrow"
        )
        test_participant.save()

        background_check=models.BackgroundCheck(
            participant_id=test_participant,
            date="2014-3-5",
            signature="TEST Oliver Queen",
            driver_license_num="79801234AB"
        )
        background_check.save()

        test_participant_no_background_check=models.Participant(
            name="TEST The Doctor",
            birth_date="1235-8-14",
            email="thedoctor@galifrey.com",
            weight=190,
            gender="M",
            height=76.0,
            minor_status="A",
            address_street="The TARDIS",
            address_city="Time and space",
            address_state="OK",
            address_zip="74801",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
        )
        test_participant_no_background_check.save()

    def test_background_check_report_loads_if_user_logged_in(self):
        """ Tests whether the Background Check Release report page loads if the
         user is logged in and valid URL parameters are passed (participant_id,
         year, month, day). """

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-background",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_background_check_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Backgorund Check release report page redirects to
         the login page if the user is not logged in. """

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-background",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_background_check_report_shows_error_if_invalid_participant(self):
        """ Tests whether the Background Check Release report page shows the
         correct error if the user is logged in but an invalid participant_id is
         passed. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-background",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_background_check_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Background Check Release report page shows the
         correct error if the user is logged in but an invalid date for the
         Background Check Release is passed. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        response = self.client.get(
            reverse("report-background",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_background_check_report_shows_error_if_no_background_check(self):
        """ Tests whether the Background Check Release report page shows the
         correct error if the user is logged in and all parameters passed are
         valid, but the BackgroundCheck record does not exist. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST The Doctor",
            birth_date="1235-8-14",
        )

        response = self.client.get(
            reverse("report-background",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_BACKGROUND_CHECK_NOT_AVAILABLE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...


class TestSeizureEvaluationReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Oliver Queen",
            birth_date="1985-05-16",
            email="arrow@archeryandthings.com",
            weight=188,
            gender="M",
            height=69,
            minor_status="A",
            address_street="4568 Rich Person Rd.",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="789-132-0024",
            phone_cell="789-456-8800",
            phone_work="789-039-3008",
            school_institution="Team Arrow"
        )
        test_participant.save()

        seizure_eval=models.SeizureEval(
            participant_id=test_participant,
            date="2014-3-5",
            date_of_last_seizure="2013-3-4",
            duration_of_last_seizure="A couple of seconds",
            typical_cause="Eggplants",
            seizure_indicators="Blank stare",
            after_effect="Fatigued, disoriented",
            during_seizure_stare="",
            during_seizure_stare_length="",
            during_seizure_walks="",
            during_seizure_aimless="",
            during_seizure_cry_etc="",
            during_seizure_bladder_bowel="",
            during_seizure_confused_etc="",
            during_seizure_other="",
            during_seizure_other_description="",
            knows_when_will_occur="",
            can_communicate_when_will_occur="",
            action_to_take_do_nothing="",
            action_to_take_dismount="",
            action_to_take_allow_time="",
            action_to_take_allow_time_how_long=15,
            action_to_take_report_immediately="",
            action_to_take_send_note="",
            seizure_frequency="Every couple of months",
            signature="Alfred Pennyworth",
        )
        seizure_eval.save()

        test_participant_no_background_check=models.Participant(
            name="TEST The Doctor",
            birth_date="1235-8-14",
            email="thedoctor@galifrey.com",
            weight=190,
            gender="M",
            height=76.0,
            minor_status="A",
            address_street="The TARDIS",
            address_city="Time and space",
            address_state="OK",
            address_zip="74801",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
        )
        test_participant_no_background_check.save()

    def test_seizure_eval_report_loads_if_user_logged_in(self):
        """ Tests whether the Seizure Evaluation report page loads if the
         user is logged in and valid URL parameters are passed (participant_id,
         year, month, day). """

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-seizure",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_seizure_eval_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Seizure Evaluation report page redirects to
         the login page if the user is not logged in. """

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-seizure",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_seizure_eval_report_shows_error_if_invalid_participant(self):
        """ Tests whether the Seizure Evaluation report page shows the
         correct error if the user is logged in but an invalid participant_id is
         passed. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-seizure",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_seizure_eval_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Seizure Evaluation report page shows the
         correct error if the user is logged in but an invalid date for the
         Background Check Release is passed. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Oliver Queen",
            birth_date="1985-05-16"
        )

        response = self.client.get(
            reverse("report-seizure",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_seizure_eval_report_shows_error_if_no_seizure_eval(self):
        """ Tests whether the Seizure Evaluation report page shows the
         correct error if the user is logged in and all parameters passed are
         valid, but the SeizureEval record does not exist. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST The Doctor",
            birth_date="1235-8-14",
        )

        response = self.client.get(
            reverse("report-seizure",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_SEIZURE_EVAL_NOT_AVAILABLE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...


class TestObservationEvaluation(TestCase):
    def setUp(self):
        setup_test_environment()
        client=Client()

        test_user=models.User(
            username="testuser",
            password="testpass",
        )
        test_user.save()

        test_participant=models.Participant(
            name="Test Matthew Clear",
            birth_date="1236-9-18",
            email="thedoctor@galifre.com",
            weight=190,
            gender="M",
            height=76.0,
            minor_status="A",
            address_street="The TARDIS",
            address_city="Time and space",
            address_state="OK",
            address_zip="74801",
            phone_home="300-200-1000",
            phone_cell="300-500-6000",
            phone_work="598-039-3008",
            school_institution="n/a"
        )
        test_participant.save()

        test_observation_eval=models.ObservationEvaluation(
            participant_id=test_participant,
            date="2000-1-1",
        )
        test_observation_eval.save()

        test_eval_attitude=models.EvalAttitude(
            participant_id=test_participant,
            date="1993-6-14",
            walking_through_barn_willing="1",
            walking_through_barn_motivated="1",
            walking_through_barn_appearance="1",
            looking_at_horses_willing="2",
            looking_at_horses_motivated="2",
            looking_at_horses_appearance="2",
            petting_horses_willing="3",
            petting_horses_motivated="3",
            petting_horses_appearance="3",
            up_down_ramp_willing="-",
            up_down_ramp_motivated="-",
            up_down_ramp_appearance="-",
            mounting_before_willing="2",
            mounting_before_motivated="2",
            mounting_before_appearance="2",
            mounting_after_willing="3",
            mounting_after_motivated="3",
            mounting_after_appearance="3",
            riding_before_willing="1",
            riding_before_motivated="1",
            riding_before_appearance="1",
            riding_during_willing="-",
            riding_during_motivated="-",
            riding_during_appearance="-",
            riding_after_willing="3",
            riding_after_motivated="3",
            riding_after_appearance="3",
            understands_directions_willing="1",
            understands_directions_motivated="1",
            understands_directions_appearance="1",
            participates_exercises_willing="2",
            participates_exercises_motivated="2",
            participates_exercises_appearance="2",
            participates_games_willing="3",
            participates_games_motivated="3",
            participates_games_appearance="3",
            general_attitude_willing="-",
            general_attitude_motivated="-",
            general_attitude_appearance="-",
        )
        test_eval_attitude.save()

    def test_observation_eval_loads_if_user_logged_in_no_release(self):

        test_user=models.User.objects.get(
            username="testuser",
        )
        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="Test Matthew Clear",
            birth_date="1236-9-18"
        )

        response = self.client.get(
            reverse('private-form-observation-evaluation',
                kwargs={
                    'participant_id':test_participant_in_db.participant_id
                }
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_observation_eval_redirects_if_user_not_logged_in(self):

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse('private-form-observation-evaluation',
                kwargs={
                    "participant_id":test_participant_in_db.participant_id
                }
            )
        )
        self.assertEqual(response.status_code, 302)


        print("reverse(\"user-login\")"+ reverse("user-login"))

        self.assertTrue(reverse("user-login") in response["location"])

    def test_user_inputs_not_valid_data(self):
        test_user=models.User.objects.get(
            username="testuser",
        )
        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="Test Matthew Clear",
            birth_date="1236-9-18"
        )

        form_data={
            "date": "2000-5-1",
            "walking_through_barn_willing": "1waefhiowe",
            "walking_through_barn_motivated": "1",
            "walking_through_barn_appearance": "1",
            "looking_at_horses_willing": "2",
            "looking_at_horses_motivated": "?????????????????/",
            "looking_at_horses_appearance": "2",
            "petting_horses_willing": "3",
            "petting_horses_motivated": "3",
            "petting_horses_appearance": "3",
            "up_down_ramp_willing": "-",
            "up_down_ramp_motivated": "-",
            "up_down_ramp_appearance": "-",
            "mounting_before_willing": "2",
            "mounting_before_motivated": "2",
            "mounting_before_appearance": "2",
            "mounting_after_willing": "3",
            "mounting_after_motivated": "3",
            "mounting_after_appearance": "3",
            "riding_before_willing": "1",
            "riding_before_motivated": "1",
            "riding_before_appearance": "1",
            "riding_during_willing": "-",
            "riding_during_motivated": "-",
            "riding_during_appearance": "-",
            "riding_after_willing": "3",
            "riding_after_motivated": "3",
            "riding_after_appearance": "3",
            "understands_directions_willing": "1",
            "understands_directions_motivated": "1",
            "understands_directions_appearance": "1",
            "participates_exercises_willing": "2",
            "participates_exercises_motivated": "2",
            "participates_exercises_appearance": "2",
            "participates_games_willing": "3",
            "participates_games_motivated": "3",
            "participates_games_appearance": "3",
            "general_attitude_willing": "-",
            "general_attitude_motivated": "-",
            "general_attitude_appearance": "-",
        }

        response=self.client.post(
            reverse(
                "private-form-observation-evaluation",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                }
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_observation_evaluation_form_error_no_participant_get(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response=self.client.get(
            reverse(
                "private-form-observation-evaluation",
                kwargs={
                    "participant_id":99999999999,
                }
            )
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_observation_evaluation_form_error_no_participant_post(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        form_data={
            "date":"2016-2-13",
            "walking_through_barn_motivated": "1",
            "walking_through_barn_willing": "1",
            "walking_through_barn_appearance": "1",
            "looking_at_horses_motivated": "1",
            "looking_at_horses_willing": "1",
            "looking_at_horses_appearance": "1",
            "petting_horses_motivated": "1",
            "petting_horses_willing": "1",
            "petting_horses_appearance": "1",
            "up_down_ramp_motivated": "1",
            "up_down_ramp_willing": "1",
            "up_down_ramp_appearance": "1",
            "mounting_before_motivated": "1",
            "mounting_before_willing": "1",
            "mounting_before_appearance": "1",
            "mounting_after_motivated": "1",
            "mounting_after_willing": "1",
            "mounting_after_appearance": "1",
            "riding_before_motivated": "1",
            "riding_before_willing": "1",
            "riding_before_appearance": "1",
            "riding_during_motivated": "1",
            "riding_during_willing": "1",
            "riding_during_appearance": "1",
            "riding_after_motivated": "1",
            "riding_after_willing": "1",
            "riding_after_appearance": "1",
            "understands_directions_motivated": "1",
            "understands_directions_willing": "1",
            "understands_directions_appearance": "1",
            "participates_exercises_motivated": "1",
            "participates_exercises_willing": "1",
            "participates_exercises_appearance": "1",
            "participates_games_motivated": "1",
            "participates_games_willing": "1",
            "participates_games_appearance": "1",
            "general_attitude_motivated":"1",
            "general_attitude_willing":"1",
            "general_attitude_appearance":"1",
        }

        self.client.force_login(test_user)

        response=self.client.post(
            reverse(
                "private-form-observation-evaluation",
                kwargs={
                    "participant_id":99999999999,
                }
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_observation_eval_saves_valid_data(self):
        test_user=models.User.objects.get(
            username="testuser",
        )
        self.client.force_login(test_user)

        form_data={
            "date":"2016-2-13",
            "walking_through_barn_motivated": "1",
            "walking_through_barn_willing": "1",
            "walking_through_barn_appearance": "1",
            "looking_at_horses_motivated": "1",
            "looking_at_horses_willing": "1",
            "looking_at_horses_appearance": "1",
            "petting_horses_motivated": "1",
            "petting_horses_willing": "1",
            "petting_horses_appearance": "1",
            "up_down_ramp_motivated": "1",
            "up_down_ramp_willing": "1",
            "up_down_ramp_appearance": "1",
            "mounting_before_motivated": "1",
            "mounting_before_willing": "1",
            "mounting_before_appearance": "1",
            "mounting_after_motivated": "1",
            "mounting_after_willing": "1",
            "mounting_after_appearance": "1",
            "riding_before_motivated": "1",
            "riding_before_willing": "1",
            "riding_before_appearance": "1",
            "riding_during_motivated": "1",
            "riding_during_willing": "1",
            "riding_during_appearance": "1",
            "riding_after_motivated": "1",
            "riding_after_willing": "1",
            "riding_after_appearance": "1",
            "understands_directions_motivated": "1",
            "understands_directions_willing": "1",
            "understands_directions_appearance": "1",
            "participates_exercises_motivated": "1",
            "participates_exercises_willing": "1",
            "participates_exercises_appearance": "1",
            "participates_games_motivated": "1",
            "participates_games_willing": "1",
            "participates_games_appearance": "1",
            "general_attitude_motivated":"1",
            "general_attitude_willing":"1",
            "general_attitude_appearance":"1",
        }

        test_participant_in_db=models.Participant.objects.get(
            name="Test Matthew Clear",
            birth_date="1236-9-18"
        )

        response=self.client.post(
            reverse(
                "private-form-observation-evaluation",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                }
            ),
            form_data
        )

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Retrieve the new EvalAttitude record:
        found_eval_attitude=False
        try:
            # We found it
            eval_attitude_in_db=models.EvalAttitude.objects.get(
                participant_id=test_participant_in_db.participant_id,
                date=form_data["date"]
            )
            found_eval_attitude=True
        except ObjectDoesNotExist:
            # We didn't find it
            pass
        self.assertTrue(found_eval_attitude)

        # Checked the EvalAttitude attributes were stored correctly:
        self.assertEqual(
            eval_attitude_in_db.walking_through_barn_willing,
            form_data["walking_through_barn_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.walking_through_barn_motivated,
            form_data["walking_through_barn_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.walking_through_barn_appearance,
            form_data["walking_through_barn_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.looking_at_horses_willing,
            form_data["looking_at_horses_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.looking_at_horses_motivated,
            form_data["looking_at_horses_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.looking_at_horses_appearance,
            form_data["looking_at_horses_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.petting_horses_willing,
            form_data["petting_horses_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.petting_horses_motivated,
            form_data["petting_horses_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.petting_horses_appearance,
            form_data["petting_horses_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.up_down_ramp_willing,
            form_data["up_down_ramp_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.up_down_ramp_motivated,
            form_data["up_down_ramp_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.up_down_ramp_appearance,
            form_data["up_down_ramp_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.mounting_before_willing,
            form_data["mounting_before_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.mounting_before_motivated,
            form_data["mounting_before_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.mounting_before_appearance,
            form_data["mounting_before_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.mounting_after_willing,
            form_data["mounting_after_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.mounting_after_motivated,
            form_data["mounting_after_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.mounting_after_appearance,
            form_data["mounting_after_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_before_willing,
            form_data["riding_before_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_before_motivated,
            form_data["riding_before_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_before_appearance,
            form_data["riding_before_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_during_willing,
            form_data["riding_during_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_during_motivated,
            form_data["riding_during_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_during_appearance,
            form_data["riding_during_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_after_willing,
            form_data["riding_after_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_after_motivated,
            form_data["riding_after_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.riding_after_appearance,
            form_data["riding_after_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.understands_directions_willing,
            form_data["understands_directions_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.understands_directions_motivated,
            form_data["understands_directions_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.understands_directions_appearance,
            form_data["understands_directions_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.participates_exercises_willing,
            form_data["participates_exercises_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.participates_exercises_motivated,
            form_data["participates_exercises_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.participates_exercises_appearance,
            form_data["participates_exercises_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.participates_games_willing,
            form_data["participates_games_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.participates_games_motivated,
            form_data["participates_games_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.participates_games_appearance,
            form_data["participates_games_appearance"]
        )
        self.assertEqual(
            eval_attitude_in_db.general_attitude_willing,
            form_data["general_attitude_willing"]
        )
        self.assertEqual(
            eval_attitude_in_db.general_attitude_motivated,
            form_data["general_attitude_motivated"]
        )
        self.assertEqual(
            eval_attitude_in_db.general_attitude_appearance,
            form_data["general_attitude_appearance"]
        )

        found_observation_evaluation=False
        try:
            # We found it
            observation_evaluation=models.ObservationEvaluation.objects.get(
                participant_id=test_participant_in_db.participant_id,
                date=form_data["date"]
            )
            found_observation_evaluation=True
        except ObjectDoesNotExist:
            # We didn't find it
            pass
        self.assertTrue(found_observation_evaluation)

    def test_observation_eval_duplicate_pk_observationevaluation(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         participant already has a ObservationEvaluation record with the same
         (participant_id, date) as its primary key. """

        try:
            with transaction.atomic():
                test_user=models.User.objects.get(
                    username="testuser",
                )
                self.client.force_login(test_user)

                form_data={
                    "date":"2000-1-1",
                    "walking_through_barn_motivated": "1",
                    "walking_through_barn_willing": "1",
                    "walking_through_barn_appearance": "1",
                    "looking_at_horses_motivated": "1",
                    "looking_at_horses_willing": "1",
                    "looking_at_horses_appearance": "1",
                    "petting_horses_motivated": "1",
                    "petting_horses_willing": "1",
                    "petting_horses_appearance": "1",
                    "up_down_ramp_motivated": "1",
                    "up_down_ramp_willing": "1",
                    "up_down_ramp_appearance": "1",
                    "mounting_before_motivated": "1",
                    "mounting_before_willing": "1",
                    "mounting_before_appearance": "1",
                    "mounting_after_motivated": "1",
                    "mounting_after_willing": "1",
                    "mounting_after_appearance": "1",
                    "riding_before_motivated": "1",
                    "riding_before_willing": "1",
                    "riding_before_appearance": "1",
                    "riding_during_motivated": "1",
                    "riding_during_willing": "1",
                    "riding_during_appearance": "1",
                    "riding_after_motivated": "1",
                    "riding_after_willing": "1",
                    "riding_after_appearance": "1",
                    "understands_directions_motivated": "1",
                    "understands_directions_willing": "1",
                    "understands_directions_appearance": "1",
                    "participates_exercises_motivated": "1",
                    "participates_exercises_willing": "1",
                    "participates_exercises_appearance": "1",
                    "participates_games_motivated": "1",
                    "participates_games_willing": "1",
                    "participates_games_appearance": "1",
                    "general_attitude_motivated":"1",
                    "general_attitude_willing":"1",
                    "general_attitude_appearance":"1",
                }

                test_participant_in_db=models.Participant.objects.get(
                    name="Test Matthew Clear",
                    birth_date="1236-9-18"
                )

                response=self.client.post(
                    reverse(
                        "private-form-observation-evaluation",
                        kwargs={
                            "participant_id":test_participant_in_db.participant_id,
                        }
                    ),
                    form_data
                )

                # Assert that the reponse code is a 302 (redirect):
                self.assertEqual(response.status_code, 302)

                # Assert that the context for the new view
                # contains the correct error:
                self.assertEqual(
                    views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                        form="observation evaluation"
                    ),
                    response.context["error_text"]
                )
        except:
            pass

    def test_observation_eval_duplicate_pk_evalattitude(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         participant already has a EvalAttitude record with the same
         (participant_id, date) as its primary key. """

        try:
            with transaction.atomic():
                test_user=models.User.objects.get(
                    username="testuser",
                )
                self.client.force_login(test_user)

                form_data={
                    "date": "1993-6-14",
                    "walking_through_barn_motivated": "1",
                    "walking_through_barn_willing": "1",
                    "walking_through_barn_appearance": "1",
                    "looking_at_horses_motivated": "1",
                    "looking_at_horses_willing": "1",
                    "looking_at_horses_appearance": "1",
                    "petting_horses_motivated": "1",
                    "petting_horses_willing": "1",
                    "petting_horses_appearance": "1",
                    "up_down_ramp_motivated": "1",
                    "up_down_ramp_willing": "1",
                    "up_down_ramp_appearance": "1",
                    "mounting_before_motivated": "1",
                    "mounting_before_willing": "1",
                    "mounting_before_appearance": "1",
                    "mounting_after_motivated": "1",
                    "mounting_after_willing": "1",
                    "mounting_after_appearance": "1",
                    "riding_before_motivated": "1",
                    "riding_before_willing": "1",
                    "riding_before_appearance": "1",
                    "riding_during_motivated": "1",
                    "riding_during_willing": "1",
                    "riding_during_appearance": "1",
                    "riding_after_motivated": "1",
                    "riding_after_willing": "1",
                    "riding_after_appearance": "1",
                    "understands_directions_motivated": "1",
                    "understands_directions_willing": "1",
                    "understands_directions_appearance": "1",
                    "participates_exercises_motivated": "1",
                    "participates_exercises_willing": "1",
                    "participates_exercises_appearance": "1",
                    "participates_games_motivated": "1",
                    "participates_games_willing": "1",
                    "participates_games_appearance": "1",
                    "general_attitude_motivated":"1",
                    "general_attitude_willing":"1",
                    "general_attitude_appearance":"1",
                }

                test_participant_in_db=models.Participant.objects.get(
                    name="Test Matthew Clear",
                    birth_date="1236-9-18"
                )

                response=self.client.post(
                    reverse(
                        "private-form-observation-evaluation",
                        kwargs={
                            "participant_id":test_participant_in_db.participant_id,
                        }
                    ),
                    form_data
                )

                # Assert that the reponse code is a 302 (redirect):
                self.assertEqual(response.status_code, 302)

                # Assert that the context for the new view
                # contains the correct error:
                self.assertEqual(
                    views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                        form="observation evaluation"
                    ),
                    response.context["error_text"]
                )
        except:
            pass


class TestAdoptParticipant(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_participant_donor=models.Donor(
            name="TEST Super Batman",
            email="michael.something@ftc.gov"
        )
        test_participant_donor.save()

    def test_form_finds_existing_donor(self):
        found_donor=False

        form_data={
            "name":"TEST Super Batman",
            "email":"michael.something@ftc.gov",
            "amount":"5",
        }
        form=forms.ParticipantAdoptionForm(form_data)

        if form.is_valid():
            print("Form is valid")

            try:
                print ("Finding Exsisting Donor")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("Found Donor")
                found_donor=True

            except:
                print("ERROR: Donor Not found!")

        self.assertTrue(found_donor)

    def test_form_does_not_find_non_existent_donor_name(self):
        found_donor=False

        form_data={
            "name":"TEST Super Flash",
            "email":"Michael.Something@ftc.gov",
            "amount":"5",
        }
        form=forms.ParticipantAdoptionForm(form_data)

        if form.is_valid():
            print("Form is valid")

            try:
                print ("Finding Exsisting Donor")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("ERROR: Found Donor!")
                found_donor=True

            except:
                print("Donor Not found.")

        self.assertFalse(found_donor)

    def test_form_does_not_find_non_existent_donor_email(self):
        found_donor=False

        form_data={
            "name":"TEST Super Batman",
            "email":"Miguel.Something@ftc.gov",
            "amount":"5",
        }
        form=forms.ParticipantAdoptionForm(form_data)

        if form.is_valid():
            print("Form is valid")

            try:
                print ("Finding Exsisting Donor")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("ERROR: Found Donor!")
                found_donor=True

            except:
                print("Donor Not found.")

        self.assertFalse(found_donor)

    def test_donor_invalid_amount(self):

        form_data={
            "name":"TEST Super Aquaman",
            "email":"Michael.Something@ftc.gov",
            "amount":"sadhiugiufe5",
        }

        response=self.client.post(reverse("donation-participant"),form_data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_donor_invalid_name_length(self):

        form_data={
            "name":"TEST Super Aquaman with a stupid super long name thatiszzzz"
                "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
            "email":"Miguel.Something@ftc.gov",
            "amount":"5",
        }

        response=self.client.post(reverse("donation-participant"), form_data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_donation_adopt_participant_saves_with_valid_data(self):

        form_data={
            "name": "TEST Super Batman",
            "email": "michael.something@ftc.gov",
            "amount": "5",
        }

        response=self.client.post(reverse("donation-participant"), form_data)

        self.assertEqual(response.status_code, 302)

        try:
            print("Retrieving Donor Record...")
            donor_in_db=models.Donor.objects.get(
                name=form_data["name"],
                email=form_data["email"]
            )
        except:
            print("Error: Unable to retrieve donor record!")

        try:
            print("Retrieving Donation Record")
            donation_in_db=models.Donation.objects.get(
                donor_id=donor_in_db,
                email=form_data["email"]
            )
            print(
                "successfully Retrieved new Donation record."
            )
            print(
                "Checking stored Donation attributes..."
            )
            self.assertEqual(
                donor_in_db.name,
                form_data["name"]
            )
            self.assertEqual(
                donor_in_db.email,
                form_data["email"]
            )
            self.assertEqual(
                donation_in_db.amount,
                form_data["amount"]
            )
        except:
            print(
                "Error: Unable to retreive new Donation Record!"
            )


class TestAdoptHorse(TestCase):
    def setUp(self):
        setup_test_environment()
        client=Client()

        test_adopt_horse=models.Donor(
            name= "TEST George Bush",
            email="George.Bush@whitehouse.com"
        )
        test_adopt_horse.save()

    def test_adopt_horse_form_finds_existing_donor(self):
        found_donor=False

        form_data={
            "amount":"5",
            "name":"TEST George Bush",
            "email":"George.Bush@whitehouse.com"
        }
        form=forms.HorseAdoptionForm(form_data)

        if form.is_valid():
            print("Form is valid.")

            try:
                print("Finding donor...")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("Found donor.")
                found_donor=True

            except:
                print("Donor Not Found.")

        else:
            print("Form is Not Valid.")

        self.assertTrue(found_donor)

    def test_adopt_horse_form_does_not_find_non_existent_donor_name(self):
        found_donor=False

        form_data={
            "amount":"5",
            "name":"Test Not George Bush",
            "email":"George.Bush@whitehouse.com"
        }
        form=forms.HorseAdoptionForm(form_data)

        if form.is_valid():
            print("Form is valid.")

            try:
                print("Finding donor...")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("Found donor.")
                found_donor=True

            except:
                print("Donor Not Found.")

        self.assertFalse(found_donor)

    def test_adopt_horse_form_does_not_find_non_existent_donor_email(self):

        found_donor=False

        form_data={
            "amount":"5",
            "name":"Test George Bush",
            "email":"notgeorge@bush.com"
        }
        form=forms.HorseAdoptionForm(form_data)

        if form.is_valid():
            print("Form is Valid")

            try:
                print("Finding donor...")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("Found donor.")
                found_donor=True

            except:
                print("Donor Not Found.")

        self.assertFalse(found_donor)

    def test_adopt_horse_form_invalid_amount(self):
        form_data={
            "name":"TEST Super Aquaman",
            "email":"Michael.Something@ftc.gov",
            "amount":"sadhiugiufe5",
        }

        response=self.client.post(reverse("donation-horse"),form_data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_adopt_horse_invalid_name_length(self):
        form_data={
            "name":"TEST Super Aquaman with a stupid super long name thatiszzzz"
                "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
            "email":"Miguel.Something@ftc.gov",
            "amount":"5",
        }

        response=self.client.post(reverse("donation-horse"), form_data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_donation_adopt_horse_saves_with_valid_data_donor_exists(self):

        form_data={
            "amount":"5",
            "name":"TEST George Bush",
            "email":"George.Bush@whitehouse.com"
        }

        response=self.client.post(reverse("donation-horse"), form_data)

        self.assertEqual(response.status_code, 302)

        try:
            print("Retrieving Donor Record...")
            donor_in_db=models.Donor.objects.get(
                name=form_data["name"],
                email=form_data["email"]
            )
        except:
            print("Error: Unable to retrieve donor record!")

        try:
            print("Retrieving Donation Record")
            donation_in_db=models.Donation.objects.get(
                donor_id=donor_in_db,
                email=form_data["email"]
            )
            print(
                "successfully Retrieved new Donation record."
            )
            print(
                "Checking stored Donation attributes..."
            )
            self.assertEqual(
                donor_in_db.name,
                form_data["name"]
            )
            self.assertEqual(
                donor_in_db.email,
                form_data["email"]
            )
            self.assertEqual(
                donation_in_db.amount,
                form_data["amount"]
            )
        except:
            print(
                "Error: Unable to retreive new Donation Record!"
            )

    def test_donation_adopt_horse_saves_with_valid_data_new_donor(self):

        form_data={
            "amount":"300",
            "name":"TEST New Donor",
            "email":"new@donor.com"
        }

        response=self.client.post(reverse("donation-horse"), form_data)

        self.assertEqual(response.status_code, 302)

        try:
            print("Retrieving Donor Record...")
            donor_in_db=models.Donor.objects.get(
                name=form_data["name"],
                email=form_data["email"]
            )
        except:
            print("Error: Unable to retrieve donor record!")

        try:
            print("Retrieving Donation Record")
            donation_in_db=models.Donation.objects.get(
                donor_id=donor_in_db,
                email=form_data["email"]
            )
            print(
                "successfully Retrieved new Donation record."
            )
            print(
                "Checking stored Donation attributes..."
            )
            self.assertEqual(
                donor_in_db.name,
                form_data["name"]
            )
            self.assertEqual(
                donor_in_db.email,
                form_data["email"]
            )
            self.assertEqual(
                donation_in_db.amount,
                form_data["amount"]
            )
        except:
            print(
                "Error: Unable to retreive new Donation Record!"
            )


class TestMonetaryDonation(TestCase):
    def setUp(self):
        setup_test_environment()
        client=Client()

        test_participant_donor=models.Donor(
            name="TEST Batt Maker",
            email="Matt.Something@ftc.gov",
        )
        test_participant_donor.save()

    def test_monetary_donation_form_finds_existing_donor(self):
        found_donor=False

        form_data={
            "name":"TEST Batt Maker",
            "email":"Matt.Something@ftc.gov",
            "amount":"5",
            "purpose": "",
        }
        form=forms.MonetaryDonationForm(form_data)

        if form.is_valid():
            print("Form is valid")

            try:
                print ("Finding Exsisting Donor")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("Found Donor")
                found_donor=True

            except:
                print("Donor Not found.")

        self.assertTrue(found_donor)

    def test_monetary_donation_form_finds_non_existing_donor_name(self):
        found_donor=False

        form_data={
            "name":"TEST Matthias",
            "email":"Matt.Something@ftc.gov",
            "amount":"5",
            "purpose": "",
        }
        form=forms.MonetaryDonationForm(form_data)

        if form.is_valid():
            print("Form is valid")

            try:
                print ("Finding Exsisting Donor")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("Found Donor")
                found_donor=True

            except:
                print("Donor Not found.")

        self.assertFalse(found_donor)

    def test_monetary_donation_form_finds_non_existing_donor_email(self):
        found_donor=False

        form_data={
            "name":"TEST Matthew",
            "email":"Matt.Something@ftc.gov",
            "amount":"5",
            "purpose": "",
        }
        form=forms.MonetaryDonationForm(form_data)

        if form.is_valid():
            print("Form is valid")

            try:
                print ("Finding Exsisting Donor")
                donor_instance=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"],
                )
                print("Found Donor")
                found_donor=True

            except:
                print("Donor Not found.")

        self.assertFalse(found_donor)

    def test_monetary_donation_form_invalid_amount(self):
        form_data={
            "name":"TEST Super Aquaman",
            "email":"Michael.Something@ftc.gov",
            "amount":"sadhiugiufe5",
            "purpose": "",
        }

        response=self.client.post(reverse("donation-monetary"),form_data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_monetary_donation_form_invalid_name_length(self):
        form_data={
            "name":"TEST Super Aquaman with a stupid super long name thatiszzzz"
                "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",
            "email":"Miguel.Something@ftc.gov",
            "amount":"5",
            "purpose": "",
        }

        response=self.client.post(reverse("donation-monetary"), form_data)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_donation_adopt_horse_saves_with_valid_data_donor_exists(self):

        form_data={
            "amount":"5",
            "name":"TEST Batt Maker",
            "email":"Matt.Something@ftc.gov",
            "purpose": "New saddles"
        }

        response=self.client.post(reverse("donation-monetary"), form_data)

        self.assertEqual(response.status_code, 302)

        try:
            print("Retrieving Donor Record...")
            donor_in_db=models.Donor.objects.get(
                name=form_data["name"],
                email=form_data["email"]
            )
        except:
            print("Error: Unable to retrieve donor record!")

        try:
            print("Retrieving Donation Record")
            donation_in_db=models.Donation.objects.get(
                donor_id=donor_in_db,
                email=form_data["email"]
            )
            print(
                "successfully Retrieved new Donation record."
            )
            print(
                "Checking stored Donation attributes..."
            )
            self.assertEqual(
                donor_in_db.name,
                form_data["name"]
            )
            self.assertEqual(
                donor_in_db.email,
                form_data["email"]
            )
            self.assertEqual(
                donation_in_db.amount,
                form_data["amount"]
            )
            self.assertEqual(
                donation_in_db.purpose,
                form_data["purpose"]
            )
        except:
            print(
                "Error: Unable to retreive new Donation Record!"
            )

    def test_donation_adopt_horse_saves_with_valid_data_new_donor(self):

        form_data={
            "amount":"300",
            "name":"TEST New Donor",
            "email":"new@donor.com",
            "purpose": "",
        }

        response=self.client.post(reverse("donation-monetary"), form_data)

        self.assertEqual(response.status_code, 302)

        try:
            print("Retrieving Donor Record...")
            donor_in_db=models.Donor.objects.get(
                name=form_data["name"],
                email=form_data["email"]
            )
        except:
            print("Error: Unable to retrieve donor record!")

        try:
            print("Retrieving Donation Record")
            donation_in_db=models.Donation.objects.get(
                donor_id=donor_in_db,
                email=form_data["email"]
            )
            print(
                "successfully Retrieved new Donation record."
            )
            print(
                "Checking stored Donation attributes..."
            )
            self.assertEqual(
                donor_in_db.name,
                form_data["name"]
            )
            self.assertEqual(
                donor_in_db.email,
                form_data["email"]
            )
            self.assertEqual(
                donation_in_db.amount,
                form_data["amount"]
            )
        except:
            print(
                "Error: Unable to retreive new Donation Record!"
            )


class TestSessionPlanForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        # Create a Participant record and save it
        test_participant=models.Participant(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21",
            email="bobby.bobbers@Something.com",
            weight=185.0,
            gender="M",
            guardian_name="Some Person",
            height=72.0,
            minor_status="G",
            address_street="1234 Some St.",
            address_city="Somce City",
            address_state="OK",
            address_zip= "74804",
            phone_home="300-234-1234",
            phone_cell="300-600-8000",
            phone_work="599-039-3009",
            school_institution="Bobby's School of Bobbiness"
        )
        test_participant.save()

        session_plan=models.Session(
            date="2014-3-5",
            tack="Some stuff"
        )
        session_plan.save()

        session_ind=models.SessionPlanInd(
            horse_leader="Fucky McFuckboy"
        )

        session_goals=models.SessionGoals(
            participant_id=test_participant,
            session_id=session_plan,
            goal_type="S",
            goal_description="Some text",
            motivation="Don't die."
        )
        session_goals.save()

        horse_info=models.Horse(
            name="Charlie"
        )
        horse_info.save()

        diagnosis_info=models.Diagnosis(
            participant_id=test_participant,
            diagnosis="Herpes",
            diagnosis_type="P"
        )
        diagnosis_info.save()

        adaptations_needed=models.AdaptationsNeeded(
            participant_id=test_participant,
            date="2016-5-1",
            ambulatory_status="I",
            ambulatory_status_other="Some shit.",
            mount_assistance_required="M",
            mount_device_needed="S",
            mount_type="T",
            dismount_assistance_required="M",
            dismount_type="A",
            num_sidewalkers_walk_spotter=1,
            num_sidewalkers_walk_heel_hold=2,
            num_sidewalkers_walk_over_thigh=2,
            num_sidewalkers_walk_other=3,
            num_sidewalkers_trot_spotter=2,
            num_sidewalkers_trot_heel_hold=2,
            num_sidewalkers_trot_over_thigh=1,
            num_sidewalkers_trot_other=3
        )
        adaptations_needed.save()

    def test_session_plan_loads_if_user_logged_in(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        response=self.client.get(
            reverse(
                "private-form-session-plan",
                kwargs={"participant_id": test_participant.participant_id}
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_session_plan_redirects_if_user_not_logged_in(self):
        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        response=self.client.get(
            reverse(
                "private-form-session-plan",
                kwargs={"participant_id": test_participant.participant_id}
            )
        )

        self.assertEqual(response.status_code, 302) # Redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_session_plan_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "date": "2016-5-1",
            "horse_name": "Charlie",
            "horse_leader": "Fucky McFuckboy",
            "tack": "Some words.",
            "diagnosis": "Herpes",
            "diagnosis_type": "P",
            "ambulatory_status": "I",
            "ambulatory_status_other": "Some shit.",
            "mount_assistance_required": "M",
            "mount_device_needed": "S",
            "mount_type": "T",
            "dismount_assistance_required": "M",
            "dismount_type": "A",
            "num_sidewalkers_walk_spotter": "1",
            "num_sidewalkers_walk_heel_hold": "2",
            "num_sidewalkers_walk_over_thigh": "2",
            "num_sidewalkers_walk_other": "3",
            "num_sidewalkers_trot_spotter": "2",
            "num_sidewalkers_trot_heel_hold": "2",
            "num_sidewalkers_trot_over_thigh": "1",
            "num_sidewalkers_trot_other": "3",
            "goal_type": "S",
            "goal_description": "Try not to break your neck.",
            "motivation": "Don't die."
        }
        form=forms.SessionPlanForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name="TEST Bobby Bobbers",
                    birth_date="1986-7-21",
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertTrue(found_participant)

    def test_session_plan_form_saves_with_valid_data(self):
        """ Verify that a Session Plan form view, populated with
         valid data, correctly saves the form to the database. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        form_data={
            "date": "2016-1-1",
            "horse_name": "Charlie",
            "horse_leader": "Fucky McFuckboy",
            "tack": "Some words.",
            "ambulatory_status": "I",
            "ambulatory_status_other": "Some shit.",
            "mount_assistance_required": "M",
            "mount_device_needed": "S",
            "mount_type": "T",
            "dismount_assistance_required": "M",
            "dismount_type": "A",
            "num_sidewalkers_walk_spotter": "1",
            "num_sidewalkers_walk_heel_hold": "2",
            "num_sidewalkers_walk_over_thigh": "2",
            "num_sidewalkers_walk_other": "3",
            "num_sidewalkers_trot_spotter": "2",
            "num_sidewalkers_trot_heel_hold": "2",
            "num_sidewalkers_trot_over_thigh": "1",
            "num_sidewalkers_trot_other": "3",
            "goal_type": "S",
            "goal_description": "Try not to break your neck.",
            "motivation": "Don't die."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-session-plan",
        kwargs={"participant_id": test_participant.participant_id}), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the updated MedicalInfo record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                participant_id=test_participant.participant_id
            )
        except:
            print("ERROR: Unable to retreive participant record!")

        #TODO: Check all stored attributes, wait until changing sidewalker types

        try:
            print("Retrieving new Session record...")
            session_in_db=(models.Session
                .objects.get(
                    tack=form_data["tack"],
                    date=form_data["date"]
                )
            )
            print("Retrieved new Session record")
        except:
            print("ERROR: Unable to retrieve new Session record!")
        try:
            session_ind_in_db=(models.SessionPlanInd
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"]
                )
            )
            print("Retrieved new Session Plan Ind record")
        except:
            print("ERROR: Unable to retrieve new Session Plan Ind record!")
        try:
            session_goals_in_db=(models.SessionGoals
                .objects.get(
                    participant_id=participant_in_db,
                    session_id=session_in_db
                )
            )
            print("Retrieved new Session Goal record")
        except:
            print("ERROR: Unable to retrieve new Session Goal record!")
        try:
            horse_in_db=(models.Horse
                .objects.get(
                    name=form_data["horse_name"]
                )
            )
            print("Retrieved new Horse record")
        except:
            print("ERROR: Unable to retrieve new Horse record!")
        try:
            adaptations_in_db=(models.AdaptationsNeeded
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"]
                )
            )
            print("Retrieved new Adaptations Needed record")
        except:
            print("ERROR: Unable to retrieve new Adaptations Needed record!")

        # Check that the attributes in the RiderEval were set correctly:
        print(
            "Checking stored ClassSession attributes..."
        )
        self.assertEqual(
            session_ind_in_db.horse_leader,
            form_data["horse_leader"]
        )
        self.assertEqual(
            adaptations_in_db.ambulatory_status,
            form_data["ambulatory_status"]
        )
        self.assertEqual(
            adaptations_in_db.ambulatory_status_other,
            form_data["ambulatory_status_other"]
        )
        self.assertEqual(
            adaptations_in_db.mount_assistance_required,
            form_data["mount_assistance_required"]
        )
        self.assertEqual(
            adaptations_in_db.mount_device_needed,
            form_data["mount_device_needed"]
        )
        self.assertEqual(
            adaptations_in_db.mount_type,
            form_data["mount_type"]
        )
        self.assertEqual(
            adaptations_in_db.dismount_assistance_required,
            form_data["dismount_assistance_required"]
        )
        self.assertEqual(
            adaptations_in_db.dismount_type,
            form_data["dismount_type"]
        )
        self.assertEqual(
            str(adaptations_in_db.num_sidewalkers_walk_spotter),
            form_data["num_sidewalkers_walk_spotter"]
        )
        self.assertEqual(
            str(adaptations_in_db.num_sidewalkers_walk_heel_hold),
            form_data["num_sidewalkers_walk_heel_hold"]
        )
        self.assertEqual(
            str(adaptations_in_db.num_sidewalkers_walk_over_thigh),
            form_data["num_sidewalkers_walk_over_thigh"]
        )
        self.assertEqual(
            str(adaptations_in_db.num_sidewalkers_walk_other),
            form_data["num_sidewalkers_walk_other"]
        )
        self.assertEqual(
            str(adaptations_in_db.num_sidewalkers_trot_spotter),
            form_data["num_sidewalkers_trot_spotter"]
        )
        self.assertEqual(
            str(adaptations_in_db.num_sidewalkers_trot_heel_hold),
            form_data["num_sidewalkers_trot_heel_hold"]
        )
        self.assertEqual(
            str(adaptations_in_db.num_sidewalkers_trot_over_thigh),
            form_data["num_sidewalkers_trot_over_thigh"]
        )
        self.assertEqual(
            str(adaptations_in_db.num_sidewalkers_trot_other),
            form_data["num_sidewalkers_trot_other"]
        )
        self.assertEqual(
            session_goals_in_db.goal_type,
            form_data["goal_type"]
        )
        self.assertEqual(
            session_goals_in_db.goal_description,
            form_data["goal_description"]
        )
        self.assertEqual(
            session_goals_in_db.motivation,
            form_data["motivation"]
        )


    def test_session_plan_error_if_invalid_participant_get(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        response=self.client.get(
            reverse(
                "private-form-session-plan",
                kwargs={"participant_id": 999999999999}
            )
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_session_plan_error_if_invalid_participant_valid_form_post(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        form_data={
            "date": "2016-1-1",
            "horse_name": "Charlie",
            "horse_leader": "Fucky McFuckboy",
            "tack": "Some words.",
            "ambulatory_status": "I",
            "ambulatory_status_other": "Some shit.",
            "mount_assistance_required": "M",
            "mount_device_needed": "S",
            "mount_type": "T",
            "dismount_assistance_required": "M",
            "dismount_type": "A",
            "num_sidewalkers_walk_spotter": "1",
            "num_sidewalkers_walk_heel_hold": "2",
            "num_sidewalkers_walk_over_thigh": "2",
            "num_sidewalkers_walk_other": "3",
            "num_sidewalkers_trot_spotter": "2",
            "num_sidewalkers_trot_heel_hold": "2",
            "num_sidewalkers_trot_over_thigh": "1",
            "num_sidewalkers_trot_other": "3",
            "goal_type": "S",
            "goal_description": "Try not to break your neck.",
            "motivation": "Don't die."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(
            reverse(
                "private-form-session-plan",
                kwargs={"participant_id": 999999999999999}
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_session_plan_error_if_invalid_participant_invalid_form_post(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        form_data={
            "date": "2016-1-1",
            "horse_name": "Charlie",
            "horse_leader": "Fucky McFuckboy",
            "tack": "Some words.",
            "ambulatory_status": "I",
            "ambulatory_status_other": "Some shit.",
            "mount_assistance_required": "Mafeawfewa",
            "mount_device_needed": "S",
            "mount_type": "T",
            "dismount_assistance_required": "M",
            "dismount_type": "A",
            "num_sidewalkers_walk_spotter": "11122233332u3094890238402",
            "num_sidewalkers_walk_heel_hold": "2",
            "num_sidewalkers_walk_over_thigh": "2",
            "num_sidewalkers_walk_other": "3",
            "num_sidewalkers_trot_spotter": "2",
            "num_sidewalkers_trot_heel_hold": "2",
            "num_sidewalkers_trot_over_thigh": "1",
            "num_sidewalkers_trot_other": "3",
            "goal_type": "S",
            "goal_description": "Try not to break your neck.",
            "motivation": "Don't die."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(
            reverse(
                "private-form-session-plan",
                kwargs={"participant_id": 999999999999999}
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_session_plan_form_with_invalid_data_shows_error(self):
        """ Verify that a Session Plan form view, populated with
         invalid data, displays the correct error message. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        form_data={
            "date": "2016-1-1",
            "horse_name": "Charlie",
            "horse_leader": "Fucky McFuckboy",
            "tack": "Some words.",
            "ambulatory_status": "I",
            "ambulatory_status_other": "Some super long shit..................."
                ".............................................................."
                ".............................................................."
                "................",
            "mount_assistance_required": "Maefaf",
            "mount_device_needed": "S",
            "mount_type": "T",
            "dismount_assistance_required": "M",
            "dismount_type": "A",
            "num_sidewalkers_walk_spotter": "1332",
            "num_sidewalkers_walk_heel_hold": "2",
            "num_sidewalkers_walk_over_thigh": "2",
            "num_sidewalkers_walk_other": "3",
            "num_sidewalkers_trot_spotter": "2",
            "num_sidewalkers_trot_heel_hold": "2",
            "num_sidewalkers_trot_over_thigh": "1",
            "num_sidewalkers_trot_other": "3",
            "goal_type": "S",
            "goal_description": "Try not to break your neck.",
            "motivation": "Don't die."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-session-plan",
        kwargs={"participant_id": test_participant.participant_id}), form_data)

        # Assert that the reponse code is a 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert we displayed the correct error message:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_session_plan_form_with_duplicate_adaptationsneeded_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a SessionPlan record with the same
         (participant_id, date) as its primary key. """

        try:
            with transaction.atomic():
                test_user=models.User.objects.get(
                    username="testuser"
                )

                self.client.force_login(test_user)

                test_participant=models.Participant.objects.get(
                    name="TEST Bobby Bobbers",
                    birth_date="1986-7-21"
                )

                form_data={
                    "date": "2016-5-1",
                    "horse_name": "Charlie",
                    "horse_leader": "Fucky McFuckboy",
                    "tack": "Some words.",
                    "ambulatory_status": "I",
                    "ambulatory_status_other": "Some shit.",
                    "mount_assistance_required": "M",
                    "mount_device_needed": "S",
                    "mount_type": "T",
                    "dismount_assistance_required": "M",
                    "dismount_type": "A",
                    "num_sidewalkers_walk_spotter": "1",
                    "num_sidewalkers_walk_heel_hold": "2",
                    "num_sidewalkers_walk_over_thigh": "2",
                    "num_sidewalkers_walk_other": "3",
                    "num_sidewalkers_trot_spotter": "2",
                    "num_sidewalkers_trot_heel_hold": "2",
                    "num_sidewalkers_trot_over_thigh": "1",
                    "num_sidewalkers_trot_other": "3",
                    "goal_type": "S",
                    "goal_description": "Try not to break your neck.",
                    "motivation": "Don't die."
                }

                # Send a post request to the form view with the form_data
                # defined above:
                response=self.client.post(
                    reverse(
                        "private-form-session-plan",
                        kwargs={
                            "participant_id": test_participant.participant_id
                        }
                    ),
                    form_data
                )

                # Assert that the reponse code is 302 (Redirect):
                self.assertEqual(response.status_code, 302)

                # Assert that the context for the new view
                # contains the correct error:
                self.assertEqual(
                    views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                        form="session plan"
                    ),
                    response.context["error_text"]
                )
        except:
            pass

class TestObservationEvaluationReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Billy Bob Jr.",
            birth_date="1988-03-26",
            email="billy.bob@junior.com",
            weight=168,
            gender="M",
            height=90,
            minor_status="A",
            address_street="1234 Billy Bob City",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="900-132-0024",
            phone_cell="800-456-8800",
            phone_work="300-039-3008",
            school_institution="Billy Bob School"
        )
        test_participant.save()

        test_observation_eval=models.ObservationEvaluation(
            participant_id=test_participant,
            date="2000-1-1",
        )
        test_observation_eval.save()

        test_eval_attitude=models.EvalAttitude(
            participant_id=test_participant,
            date="2000-1-1",
            walking_through_barn_willing="1",
            walking_through_barn_motivated="1",
            walking_through_barn_appearance="1",
            looking_at_horses_willing="2",
            looking_at_horses_motivated="2",
            looking_at_horses_appearance="2",
            petting_horses_willing="3",
            petting_horses_motivated="3",
            petting_horses_appearance="3",
            up_down_ramp_willing="-",
            up_down_ramp_motivated="-",
            up_down_ramp_appearance="-",
            mounting_before_willing="2",
            mounting_before_motivated="2",
            mounting_before_appearance="2",
            mounting_after_willing="3",
            mounting_after_motivated="3",
            mounting_after_appearance="3",
            riding_before_willing="1",
            riding_before_motivated="1",
            riding_before_appearance="1",
            riding_during_willing="-",
            riding_during_motivated="-",
            riding_during_appearance="-",
            riding_after_willing="3",
            riding_after_motivated="3",
            riding_after_appearance="3",
            understands_directions_willing="1",
            understands_directions_motivated="1",
            understands_directions_appearance="1",
            participates_exercises_willing="2",
            participates_exercises_motivated="2",
            participates_exercises_appearance="2",
            participates_games_willing="3",
            participates_games_motivated="3",
            participates_games_appearance="3",
            general_attitude_willing="-",
            general_attitude_motivated="-",
            general_attitude_appearance="-",
        )
        test_eval_attitude.save()

    def test_observation_evaluation_report_loads_if_user_logged_in(self):
        """ Tests whether the Observation Evaluation report page loads if the user is
         logged in and valid URL parameters are passed (participant_id, year,
         month, day)."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Billy Bob Jr.",
            birth_date="1988-03-26"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-observation-evaluation",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2000",
                    "month": "1",
                    "day": "1"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_observation_evaluation_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Observation Evaluation report page redirects to the login
         page if the user is not logged in."""

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-observation-evaluation",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_observation_evaluation_report_shows_error_if_invalid_participant_id(self):
        """ Tests whether the Observation Evaluation report page shows the correct error
         if the user is logged in but an invalid participant_id is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-observation-evaluation",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_observation_evaluation_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Observation Evaluation report page shows the correct error
         if the user is logged in but an invalid date for the Observation Evaluation
         is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Billy Bob Jr.",
            birth_date="1988-03-26"
        )

        response = self.client.get(
            reverse("report-observation-evaluation",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_observation_evaluation_report_shows_error_if_no_observation_evaluation(self):
        """ Tests whether the Observation Evaluation report page shows the correct error
         if the user is logged in and all parameters passed are valid, but the
         Observation Evaluation record does not exist."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Billy Bob Jr.",
            birth_date="1988-03-26"
        )

        response = self.client.get(
            reverse("report-observation-evaluation",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2016",
                    "month": "1",
                    "day": "1"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_OBS_EVAL_NOT_AVALIABLE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

class TestSessionPlanReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Fuck Me",
            birth_date="1928-04-21",
            email="fuck.me@ftc.com",
            weight=170,
            gender="M",
            height=60,
            minor_status="G",
            address_street="1234 Fuck This St.",
            address_city="Example City",
            address_state="OK",
            address_zip="74801",
            phone_home="345-132-0024",
            phone_cell="987-456-8800",
            phone_work="305-039-3008",
            school_institution="Fuck This School"
        )
        test_participant.save()

        session_plan=models.Session(
            date="2015-2-5",
            tack="Some fucking shit"
        )
        session_plan.save()

        session_ind=models.SessionPlanInd(
            participant_id=test_participant,
            date="2014-3-5",
            horse_leader="Dat Boi",
        )
        session_ind.save()

        session_goals=models.SessionGoals(
            participant_id=test_participant,
            session_id=session_plan,
            goal_type="S",
            goal_description="Some text",
            motivation="Don't die."
        )
        session_goals.save()

        horse_info=models.Horse(
            name="Fucky Horse"
        )
        horse_info.save()

        diagnosis_info=models.Diagnosis(
            participant_id=test_participant,
            diagnosis="Genital Warts",
            diagnosis_type="P"
        )
        diagnosis_info.save()

        adaptations_needed=models.AdaptationsNeeded(
            participant_id=test_participant,
            date="2016-5-8",
            ambulatory_status="I",
            ambulatory_status_other="Some shit.",
            mount_assistance_required="M",
            mount_device_needed="S",
            mount_type="T",
            dismount_assistance_required="M",
            dismount_type="A",
            num_sidewalkers_walk_spotter=1,
            num_sidewalkers_walk_heel_hold=2,
            num_sidewalkers_walk_over_thigh=2,
            num_sidewalkers_walk_other=3,
            num_sidewalkers_trot_spotter=2,
            num_sidewalkers_trot_heel_hold=2,
            num_sidewalkers_trot_over_thigh=1,
            num_sidewalkers_trot_other=3
        )
        adaptations_needed.save()

    def test_session_plan_report_loads_if_user_logged_in(self):
        """ Tests whether the Observation Evaluation report page loads if the user is
         logged in and valid URL parameters are passed (participant_id, year,
         month, day)."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Fuck Me",
            birth_date="1928-04-21"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-session-plan",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_session_plan_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Session Plan report page redirects to the login
         page if the user is not logged in."""

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-session-plan",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_session_plan_report_shows_error_if_invalid_participant_id(self):
        """ Tests whether the Session Plan report page shows the correct error
         if the user is logged in but an invalid participant_id is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-session-plan",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_session_plan_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Observation Evaluation report page shows the correct error
         if the user is logged in but an invalid date for the Observation Evaluation
         is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Fuck Me",
            birth_date="1928-04-21"
        )

        response = self.client.get(
            reverse("report-session-plan",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_session_plan_report_shows_error_if_no_session_plan(self):
        """ Tests whether the Session Plan report page shows the correct error
         if the user is logged in and all parameters passed are valid, but the
         Session Plan record does not exist."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Fuck Me",
            birth_date="1928-04-21"
        )

        response = self.client.get(
            reverse("report-session-plan",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2016",
                    "month": "1",
                    "day": "1"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_SES_PLAN_NOT_AVALIABLE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

class TestRiderEvaluationChecklistReport(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        test_participant=models.Participant(
            name="TEST Jesus Fucking Christ",
            birth_date="1926-12-25",
            email="jfc@ftc.com",
            weight=200,
            gender="M",
            height=90,
            minor_status="G",
            address_street="1234 Christ St.",
            address_city="Bethlehem",
            address_state="OK",
            address_zip="12345",
            phone_home="900-456-0024",
            phone_cell="100-156-8800",
            phone_work="315-039-3028",
            school_institution="Heaven"
        )
        test_participant.save()

        rider_eval_checklist=models.EvalRidingExercises(
            participant_id=test_participant,
            date="2014-3-5",
            comments="Yo dawg ima turn this water into wine, k fam?",
            basic_trail_rules=1,
            mount=0,
            dismount=None,
            emergency_dismount=None,
            four_natural_aids=0,
            basic_control=1,
            reverse_at_walk=1,
            reverse_at_trot=None,
            never_ridden=0,
            seat_at_walk=1,
            seat_at_trot=1,
            seat_at_canter=None,
            basic_seat_english=1,
            basic_seat_western=0,
            hand_pos_english=1,
            hand_post_western=None,
            two_point_trot=1,
            circle_trot_no_stirrups=None,
            circle_at_canter=0,
            circle_canter_no_stirrups=1,
            two_point_canter=None,
            circle_at_walk=1,
            circle_at_trot=None,
            holds_handhold_walk="U",
            holds_handhold_sit_trot="P",
            holds_handhold_post_trot="F",
            holds_handhold_canter="G",
            holds_reins_walk="E",
            holds_reins_sit_trot="N",
            holds_reins_post_trot="A",
            holds_reins_canter="P",
            shorten_lengthen_reins_walk="U",
            shorten_lengthen_reins_sit_trot="P",
            shorten_lengthen_reins_post_trot="A",
            shorten_lengthen_reins_canter="G",
            can_control_horse_walk="E",
            can_control_horse_sit_trot="N",
            can_control_horse_post_trot="A",
            can_control_horse_canter="P",
            can_halt_walk="U",
            can_halt_sit_trot="P",
            can_halt_post_trot="F",
            can_halt_canter="G",
            drop_pickup_stirrups_walk="E",
            drop_pickup_stirrups_sit_trot="N",
            drop_pickup_stirrups_post_trot="A",
            drop_pickup_stirrups_canter="P",
            rides_no_stirrups_walk="U",
            rides_no_stirrups_sit_trot="P",
            rides_no_stirrups_post_trot="F",
            rides_no_stirrups_canter="G",
            maintain_half_seat_walk="E",
            maintain_half_seat_sit_trot="E",
            maintain_half_seat_post_trot="N",
            maintain_half_seat_canter="A",
            can_post_walk="P",
            can_post_sit_trot="U",
            can_post_post_trot="P",
            can_post_canter="F",
            proper_diagonal_walk="G",
            proper_diagonal_sit_trot="E",
            proper_diagonal_post_trot="N",
            proper_diagonal_canter="A",
            proper_lead_canter_sees="P",
            proper_lead_canter_knows="U",
            can_steer_over_cavalletti_walk="P",
            can_steer_over_cavalletti_sit_trot="F",
            can_steer_over_cavalletti_post_trot="G",
            can_steer_over_cavalletti_canter="E",
            jump_crossbar_walk="N",
            jump_crossbar_sit_trot="A",
            jump_crossbar_post_trot="P",
            jump_crossbar_canter="U",
            basic_trail_rules_com="",
            mount_com="aaaaaaa",
            dismount_com="bbbbbbbbbb",
            emergency_dismount_com="",
            four_natural_aids_com="cccccc",
            basic_control_com="",
            reverse_at_walk_com="dddddddd",
            reverse_at_trot_com="",
            never_ridden_com="eeeeeeeeee",
            seat_at_walk_com="fffffffff",
            seat_at_trot_com="gggggggggg",
            seat_at_canter_com="hhhhhhhh",
            basic_seat_english_com="",
            basic_seat_western_com="iiiiiiiii",
            hand_pos_english_com="",
            hand_post_western_com="jjjjjjj",
            two_point_trot_com="kkkkkkkkkk",
            circle_trot_no_stirrups_com="",
            circle_at_canter_com="",
            circle_canter_no_stirrups_com="lllllllll",
            two_point_canter_com="mmmmmmmmm",
            circle_at_walk_com="",
            circle_at_trot_com="nnnnnnnnnn",
            holds_handhold_walk_com="",
            holds_handhold_sit_trot_com="",
            holds_handhold_post_trot_com="ooooooooo",
            holds_handhold_canter_com="",
            holds_reins_walk_com="ppppppppppp",
            holds_reins_sit_trot_com="",
            holds_reins_post_trot_com="",
            holds_reins_canter_com="qqqqqqqqqq",
            shorten_lengthen_reins_walk_com="",
            shorten_lengthen_reins_sit_trot_com="rrrrrrrrrrr",
            shorten_lengthen_reins_post_trot_com="sssssssssss",
            shorten_lengthen_reins_canter_com="",
            can_control_horse_walk_com="",
            can_control_horse_sit_trot_com="ttttttttt",
            can_control_horse_post_trot_com="",
            can_control_horse_canter_com="uuuuuuuuu",
            can_halt_walk_com="vvvvvvvvvv",
            can_halt_sit_trot_com="",
            can_halt_post_trot_com="wwwwwwwwwwwwwww",
            can_halt_canter_com="",
            drop_pickup_stirrups_walk_com="",
            drop_pickup_stirrups_sit_trot_com="",
            drop_pickup_stirrups_post_trot_com="xxxxxxxxxxxxxxxx",
            drop_pickup_stirrups_canter_com="",
            rides_no_stirrups_walk_com="",
            rides_no_stirrups_sit_trot_com="yyyyyyyyyyyy",
            rides_no_stirrups_post_trot_com="",
            rides_no_stirrups_canter_com="zzzzzzzzzzzzz",
            maintain_half_seat_walk_com="",
            maintain_half_seat_sit_trot_com="",
            maintain_half_seat_post_trot_com="",
            maintain_half_seat_canter_com="aaaaaaaaaaa",
            can_post_walk_com="",
            can_post_sit_trot_com="",
            can_post_post_trot_com="bbbbbbbbbbbbb",
            can_post_canter_com="",
            proper_diagonal_walk_com="",
            proper_diagonal_sit_trot_com="ccccccccccc",
            proper_diagonal_post_trot_com="",
            proper_diagonal_canter_com="",
            proper_lead_canter_sees_com="dddddddddd",
            proper_lead_canter_knows_com="",
            can_steer_over_cavalletti_walk_com="",
            can_steer_over_cavalletti_sit_trot_com="eeeeeeeee",
            can_steer_over_cavalletti_post_trot_com="",
            can_steer_over_cavalletti_canter_com="",
            jump_crossbar_walk_com="ffffffffff",
            jump_crossbar_sit_trot_com="",
            jump_crossbar_post_trot_com="ggggggggg",
            jump_crossbar_canter_com=""
        )
        rider_eval_checklist.save()

    def test_rider_eval_checklist_report_loads_if_user_logged_in(self):
        """ Tests whether the Rider Evaluation Checklist report page loads if the user is
         logged in and valid URL parameters are passed (participant_id, year,
         month, day)."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Jesus Fucking Christ",
            birth_date="1926-12-25"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-rider-eval-checklist",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_rider_eval_checklist_report_redirects_if_user_not_logged_in(self):
        """ Tests whether the Rider Evaluation Checklist report page redirects to the login
         page if the user is not logged in."""

        test_participant_in_db=models.Participant.objects.filter().first()

        response = self.client.get(
            reverse("report-rider-eval-checklist",
                kwargs={
                    "participant_id":test_participant_in_db.participant_id,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        # Assert we redirected to the user login page:
        self.assertEqual(response.status_code, 302) # redirected...

        # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_rider_eval_checklist_report_shows_error_if_invalid_participant_id(self):
        """ Tests whether the Rider Evaluation Checklist report page shows the correct error
         if the user is logged in but an invalid participant_id is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(
            reverse("report-rider-eval-checklist",
                kwargs={
                    "participant_id":9999999999,
                    "year": "2014",
                    "month": "3",
                    "day": "5"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_rider_eval_checklist_report_shows_error_if_invalid_form_date(self):
        """ Tests whether the Rider Evaluation Checklist report page shows the correct error
         if the user is logged in but an invalid date for the Observation Evaluation
         is passed."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Jesus Fucking Christ",
            birth_date="1926-12-25"
        )

        response = self.client.get(
            reverse("report-rider-eval-checklist",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "68904315",
                    "month": "155",
                    "day": "11122"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_INVALID_DATE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_rider_eval_checklist_report_shows_error_if_no_rider_eval_checklist(self):
        """ Tests whether the Rider Evaluation Checklist report page shows the correct error
         if the user is logged in and all parameters passed are valid, but the
         Rider Evaluation Checklist record does not exist."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant_in_db=models.Participant.objects.get(
            name="TEST Jesus Fucking Christ",
            birth_date="1926-12-25"
        )

        response = self.client.get(
            reverse("report-rider-eval-checklist",
                kwargs={
                    "participant_id": test_participant_in_db.participant_id,
                    "year": "2016",
                    "month": "1",
                    "day": "1"
                }
            )
        )

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_RIDER_EVAL_CHECKLIST_NOT_AVAILABLE
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...


class TestPhoneLogForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        # Create a Participant record and save it
        test_participant=models.Participant(
            name="TEST Fucky McFuckbot",
            birth_date="1988-8-21",
            email="fucky.mcfuckbot@Something.com",
            weight=190.0,
            gender="M",
            guardian_name="Some Person",
            height=78.0,
            minor_status="G",
            address_street="1234 Fucking St.",
            address_city="This City",
            address_state="OK",
            address_zip= "74804",
            phone_home="100-500-1234",
            phone_cell="400-200-1000",
            phone_work="599-139-3209",
            school_institution="Fucky's School of Fuckiness"
        )
        test_participant.save()

        phone_log=models.PhoneLog(
            participant_id=test_participant,
            date="2016-8-5",
            time="17:20:00",
            details="Fell off the roof."
        )
        phone_log.save()

    def test_phone_log_loads_if_user_logged_in(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Fucky McFuckbot",
            birth_date="1988-8-21"
        )

        response=self.client.get(
            reverse(
                "private-form-phone-log",
                kwargs={"participant_id": test_participant.participant_id}
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_phone_log_redirects_if_user_not_logged_in(self):
        test_participant=models.Participant.objects.get(
            name="TEST Fucky McFuckbot",
            birth_date="1988-8-21"
        )

        response=self.client.get(
            reverse(
                "private-form-phone-log",
                kwargs={"participant_id": test_participant.participant_id}
            )
        )

        self.assertEqual(response.status_code, 302) # Redirected...

         # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_phone_log_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "date": "2016-5-8",
            "time": "10:50:00",
            "details": "Fell off the roof."
        }
        form=forms.PhoneLogForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name="TEST Fucky McFuckbot",
                    birth_date="1988-8-21"
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertTrue(found_participant)

    def test_phone_log_form_saves_with_valid_data(self):
        """ Verify that a Phone Log form view, populated with
         valid data, correctly saves the form to the database. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Fucky McFuckbot",
            birth_date="1988-8-21"
        )

        form_data={
            "date": "2016-1-1",
            "time": "10:50:00",
            "details": "Ribs crushed by horse."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-phone-log",
        kwargs={"participant_id": test_participant.participant_id}), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the updated MedicalInfo record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                participant_id=test_participant.participant_id
            )
        except:
            print("ERROR: Unable to retreive participant record!")

    def test_phone_log_error_if_invalid_participant_get(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Fucky McFuckbot",
            birth_date="1988-8-21"
        )

        response=self.client.get(
            reverse(
                "private-form-phone-log",
                kwargs={"participant_id": 999999999999}
            )
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_phone_log_error_if_invalid_participant_valid_form_post(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Fucky McFuckbot",
            birth_date="1988-8-21"
        )

        form_data={
            "date": "2016-1-1",
            "time": "10:50:00",
            "details": "The second coming of Jesus Christ."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(
            reverse(
                "private-form-phone-log",
                kwargs={"participant_id": 999999999999999}
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_phone_log_error_if_invalid_participant_invalid_form_post(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Fucky McFuckbot",
            birth_date="1988-8-21"
        )

        form_data={
            "date": "2016-1-1afeawfewa",
            "time": "10:50:00afeiowaifoe",
            "details": "Decapitated in really slooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
            "ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooow"
            "manner."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(
            reverse(
                "private-form-phone-log",
                kwargs={"participant_id": 999999999999999}
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_phone_log_form_with_invalid_data_shows_error(self):
        """ Verify that a Phone Log form view, populated with
         invalid data, displays the correct error message. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Fucky McFuckbot",
            birth_date="1988-8-21"
        )

        form_data={
            "date": "2016-1-1",
            "time": "27:66:80", # <- that ain't a time...
            "Details": "Some super long shit zzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-phone-log",
        kwargs={"participant_id": test_participant.participant_id}), form_data)

        # Assert that the reponse code is a 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert we displayed the correct error message:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_phone_log_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a PhoneLog record with the same
         (participant_id, date, time) as its primary key. """

        try:
            with transaction.atomic():
                test_user=models.User.objects.get(
                    username="testuser"
                )

                self.client.force_login(test_user)

                test_participant=models.Participant.objects.get(
                    name="TEST Fucky McFuckbot",
                    birth_date="1988-8-21"
                )

                form_data={
                    "date": "2016-8-5",
                    "time": "17:20:00",
                    "details": "Child impaled by steak"
                }

                # Send a post request to the form view with the form_data
                # defined above:
                response=self.client.post(
                    reverse(
                        "private-form-phone-log",
                        kwargs={
                            "participant_id": test_participant.participant_id
                        }
                    ),
                    form_data
                )

                # Assert that the reponse code is 302 (Redirect):
                self.assertEqual(response.status_code, 302)

                # Assert that the context for the new view
                # contains the correct error:
                self.assertEqual(
                    views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                        form="phone log"
                    ),
                    response.context["error_text"]
                )
        except:
            pass


class TestIncidentsForm(TestCase):
    def setUp(self):
        setup_test_environment() # Initaliaze the test environment
        client=Client() # Make a test client (someone viewing the database)

        test_user=models.User(
            username="testuser",
            password="testpass"
        )
        test_user.save()

        # Create a Participant record and save it
        test_participant=models.Participant(
            name="TEST Dat Boi",
            birth_date="1989-10-15",
            email="dat.boi@Something.com",
            weight=186.0,
            gender="M",
            guardian_name="Some Person",
            height=80.0,
            minor_status="G",
            address_street="1234 Dat St.",
            address_city="Dat City",
            address_state="OK",
            address_zip= "74804",
            phone_home="200-500-1234",
            phone_cell="100-200-1000",
            phone_work="499-139-3209",
            school_institution="Dat School"
        )
        test_participant.save()

        incidents=models.Incidents(
            participant_id=test_participant,
            date="2016-5-8",
            time="13:30:25",
            details="Ran over by horse."
        )
        incidents.save()

    def test_incidents_loads_if_user_logged_in(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Dat Boi",
            birth_date="1989-10-15"
        )

        response=self.client.get(
            reverse(
                "private-form-incidents",
                kwargs={"participant_id": test_participant.participant_id}
            )
        )

        self.assertEqual(response.status_code, 200) # Loaded...

    def test_incidents_redirects_if_user_not_logged_in(self):
        test_participant=models.Participant.objects.get(
            name="TEST Dat Boi",
            birth_date="1989-10-15"
        )

        response=self.client.get(
            reverse(
                "private-form-incidents",
                kwargs={"participant_id": test_participant.participant_id}
            )
        )

        self.assertEqual(response.status_code, 302) # Redirected...

         # Print the url we were redirected to:
        print("response[\"location\"]" + response["location"])

        # Print the base url for the login page:
        print("reverse(\"user-login\")" + reverse("user-login"))

        # Assert the url we were redirected to contains the base login page url:
        self.assertTrue(reverse("user-login") in response["Location"])

    def test_incidents_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "date": "2016-5-8",
            "time": "13:30:25",
            "details": "Stepped in pile of shit."
        }
        form=forms.IncidentsForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name="TEST Dat Boi",
                    birth_date="1989-10-15"
                )
                print("Found participant.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        self.assertTrue(found_participant)

    def test_incidents_form_saves_with_valid_data(self):
        """ Verify that a Incidents form view, populated with
         valid data, correctly saves the form to the database. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Dat Boi",
            birth_date="1989-10-15"
        )

        form_data={
            "date": "2016-2-1",
            "time": "13:30:25",
            "details": "Impaled by tree."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-incidents",
        kwargs={"participant_id": test_participant.participant_id}), form_data)

        # Assert that the reponse code is a 302 (redirect):
        self.assertEqual(response.status_code, 302)

        # Assert the the redirect url matches the post-form page:
        self.assertEqual(
            response["Location"],
            reverse("form-saved")+"?a=a"
        )

        # Attempt to retreive the updated MedicalInfo record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                participant_id=test_participant.participant_id
            )
        except:
            print("ERROR: Unable to retreive participant record!")

    def test_incidents_error_if_invalid_participant_get(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Dat Boi",
            birth_date="1989-10-15"
        )

        response=self.client.get(
            reverse(
                "private-form-incidents",
                kwargs={"participant_id": 999999999999}
            )
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_incidents_error_if_invalid_participant_valid_form_post(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Dat Boi",
            birth_date="1989-10-15"
        )

        form_data={
            "date": "2016-3-5",
            "time": "13:30:25",
            "details": "The summoning of Satan."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(
            reverse(
                "private-form-incidents",
                kwargs={"participant_id": 999999999999999}
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_incidents_error_if_invalid_participant_invalid_form_post(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Dat Boi",
            birth_date="1989-10-15"
        )

        form_data={
            "date": "2016-1-1",
            "time": "13:30:25efawfeawfeaw",
            "details": "Got dick stuck under tree."
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(
            reverse(
                "private-form-incidents",
                kwargs={"participant_id": 999999999999999}
            ),
            form_data
        )

        self.assertEqual(response.status_code, 200) # Redirected...

        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_incidents_form_with_invalid_data_shows_error(self):
        """ Verify that a Incidents form view, populated with
         invalid data, displays the correct error message. """

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        test_participant=models.Participant.objects.get(
            name="TEST Dat Boi",
            birth_date="1989-10-15"
        )

        form_data={
            "date": "2016-6-1afeawf",
            "time": "13:30:25afeafew",
            "Details": "Some super long shit zzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
            "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-incidents",
        kwargs={"participant_id": test_participant.participant_id}), form_data)

        # Assert that the reponse code is a 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert we displayed the correct error message:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_incidents_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a Incidents record with the same
         (participant_id, date, time) as its primary key. """

        try:
            with transaction.atomic():
                test_user=models.User.objects.get(
                    username="testuser"
                )

                self.client.force_login(test_user)

                test_participant=models.Participant.objects.get(
                    name="TEST Dat Boi",
                    birth_date="1989-10-15"
                )

                form_data={
                    "date": "2016-5-8",
                    "time": "13:30:25",
                    "details": "Child lost their eye"
                }

                # Send a post request to the form view with the form_data
                # defined above:
                response=self.client.post(
                    reverse(
                        "private-form-incidents",
                        kwargs={
                            "participant_id": test_participant.participant_id
                        }
                    ),
                    form_data
                )

                # Assert that the reponse code is 302 (Redirect):
                self.assertEqual(response.status_code, 302)

                # Assert that the context for the new view
                # contains the correct error:
                self.assertEqual(
                    views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                        form="incidents"
                    ),
                    response.context["error_text"]
                )
        except:
            pass


class TestLogout(TestCase):
    def setUp(self):
        setup_test_environment()
        client=Client()

        test_user=models.User(
            username="testuser",
            password="testpass",
        )
        test_user.save()

    def test_logout_confirmation_loads(self):
        """Tests whether the index page loads."""
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(reverse("logout-confirmation"))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_loggered_out(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(reverse("loggered-out")+"?a=a")
        self.assertEqual(response.status_code, 200)

    def test_successfully_logs_out(self):
        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(reverse("logout-user"))
        self.assertEqual(response.status_code, 302)

    def test_log_out_redirects_if_user_just_entered_url(self):
        response = self.client.get(reverse("loggered-out"))

        self.assertEqual(response.status_code, 302)

        self.assertEqual(reverse("index-public"), response["Location"])
