# PURPOSE: This file contains all of the test that are run by Shippable.

from datetime import *
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
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

    def test_application_form_creates_participant(self):
        """ Tests whether the form creates a participant record once all
            fields are entered. """

        form_data={
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

        # DISABLED: We don't have a post form url redirect location or view yet
        # Assert the the redirect url matches the post-form page:
        # self.assertEqual(
        #     resp['Location'],
        #     'http://testserver/thank you place'
        # )

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

    def test_application_form_participant_already_exists(self):
        """ Form throws error if the participant already exists. """

        form_data={
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
            allergies_conditions_that_exclude=False,
            heat_exhaustion_stroke=False,
            tetanus_shot_last_ten_years=True,
            seizures_last_six_monthes=False,
            doctor_concered_re_horse_activites=False,
            physical_or_mental_issues_affecting_riding=False,
            restriction_for_horse_activity_last_five_years=False,
            present_restrictions_for_horse_activity=False,
            limiting_surgeries_last_six_monthes=False,
            signature="TEST Bruce Wayne",
            currently_taking_any_medication=False
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
            allergies_conditions_that_exclude=False,
            heat_exhaustion_stroke=False,
            tetanus_shot_last_ten_years=True,
            seizures_last_six_monthes=False,
            doctor_concered_re_horse_activites=False,
            physical_or_mental_issues_affecting_riding=False,
            restriction_for_horse_activity_last_five_years=False,
            present_restrictions_for_horse_activity=False,
            limiting_surgeries_last_six_monthes=False,
            signature="TEST Bruce Wayne",
            currently_taking_any_medication=False
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
            allergies_conditions_that_exclude=False,
            heat_exhaustion_stroke=False,
            tetanus_shot_last_ten_years=True,
            seizures_last_six_monthes=False,
            doctor_concered_re_horse_activites=False,
            physical_or_mental_issues_affecting_riding=False,
            restriction_for_horse_activity_last_five_years=False,
            present_restrictions_for_horse_activity=False,
            limiting_surgeries_last_six_monthes=False,
            signature="TEST Oliver Queen",
            currently_taking_any_medication=False
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }
        form=forms.MedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["signature"],
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST I'm Batman!",
            "date": "2016-3-30"
        }
        form=forms.MedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["signature"],
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1000-1-1",
            "signature": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }
        form=forms.MedicalReleaseForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Finding participant...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["signature"],
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Bruce Wayne",
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
                name=form_data["signature"],
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Not Bruce Wayne",
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1455-9-30",
            "signature": "TEST Bruce Wayne",
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Bruce Wayne",
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "",
            "medication_two_reason": "",
            "medication_two_frequency": "",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            # TODO: description of present restriction description/etc.
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Bruce Wayne",
            "date": "2016-3-30"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-med-release"), form_data)

        # Attempt to retrieve the new Participant record:
        try:
            print("Retrieving participant record...")
            participant_in_db=models.Participant.objects.get(
                name=form_data["signature"],
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
            "allergies_conditions_that_exclude": True,
            "allergies_conditions_that_exclude_description": "Asthma and other"
                "things and stuff.",
            "heat_exhaustion_stroke": False,
            "tetanus_shot_last_ten_years": True,
            "seizures_last_six_monthes": False,
            "currently_taking_any_medication": True,
            "medication_one_name": "Excedrin",
            "medication_one_reason": "Headaches",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_reason": "Toothaches",
            "medication_two_frequency": "3-4 hours (as needed)",
            "doctor_concered_re_horse_activites": True,
            "physical_or_mental_issues_affecting_riding": True,
            "physical_or_mental_issues_affecting_riding_description":
                "Shoulder injury requires medication for pain.",
            "restriction_for_horse_activity_last_five_years": False,
            "restriction_for_horse_activity_last_five_years_description": "",
            "present_restrictions_for_horse_activity": True,
            "limiting_surgeries_last_six_monthes": False,
            "limiting_surgeries_last_six_monthes_description": "",
            "birth_date": "1984-6-24",
            "signature": "TEST Bruce Wayne",
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "",
            "seizure_name_three": "",
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "",
            "seizure_name_three": "",
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "",
            "seizure_name_three": "",
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "Super sciency name",
            "seizure_name_three": "",
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

        # Retrieve the SeizureType record matching seizure_name_one:
        found_seizure_one=False
        try:
            print("Retrieving seizure name/type one...")
            seizure_type_one_in_db=models.SeizureType.objects.get(
                seizure_eval=seizure_eval_in_db,
                name=form_data["seizure_name_one"]
            )
            found_seizure_one=True
        except:
            print("ERROR: Could't retrieve seizure name/type one!")
        self.assertTrue(found_seizure_one)

        # Retrieve the SeizureType record matching seizure_name_two:
        found_seizure_two=False
        try:
            print("Retrieving seizure name/type two...")
            seizure_type_two_in_db=models.SeizureType.objects.get(
                seizure_eval=seizure_eval_in_db,
                name=form_data["seizure_name_two"]
            )
            found_seizure_two=True
        except:
            print("ERROR: Could't retrieve seizure name/type two!")
        self.assertTrue(found_seizure_two)

        # Retrieve the SeizureType record matching seizure_name_three:
        found_seizure_three=False
        try:
            print("Retrieving seizure name/type three...")
            seizure_type_three_in_db=models.SeizureType.objects.get(
                seizure_eval=seizure_eval_in_db,
                name=form_data["seizure_name_three"]
            )
            found_seizure_three=True
            print("ERROR: Retrieved seizure name/type three!")
        except:
            print("Could't retrieve seizure name/type three. This is the"
                " expected result")
        self.assertFalse(found_seizure_three)

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

    def test_seizure_evaluation_form_saves_seizuretype_records(self):
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "Super sciency name",
            "seizure_name_three": "Puppymonkeybaby",
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

        # Retrieve the SeizureType record matching seizure_name_one:
        found_seizure_one=False
        try:
            print("Retrieving seizure name/type one...")
            seizure_type_one_in_db=models.SeizureType.objects.get(
                seizure_eval=seizure_eval_in_db,
                name=form_data["seizure_name_one"]
            )
            found_seizure_one=True
        except:
            print("ERROR: Could't retrieve seizure name/type one!")
        self.assertTrue(found_seizure_one)

        # Retrieve the SeizureType record matching seizure_name_two:
        found_seizure_two=False
        try:
            print("Retrieving seizure name/type two...")
            seizure_type_two_in_db=models.SeizureType.objects.get(
                seizure_eval=seizure_eval_in_db,
                name=form_data["seizure_name_two"]
            )
            found_seizure_two=True
        except:
            print("ERROR: Could't retrieve seizure name/type two!")
        self.assertTrue(found_seizure_two)

        # Retrieve the SeizureType record matching seizure_name_three:
        found_seizure_three=False
        try:
            print("Retrieving seizure name/type one...")
            seizure_type_three_in_db=models.SeizureType.objects.get(
                seizure_eval=seizure_eval_in_db,
                name=form_data["seizure_name_three"]
            )
            found_seizure_three=True
        except:
            print("ERROR: Could't retrieve seizure name/type three!")
        self.assertTrue(found_seizure_three)

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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "",
            "seizure_name_three": "",
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "",
            "seizure_name_three": "",
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "",
            "seizure_name_three": "",
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "",
            "seizure_name_three": "",
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
            "seizure_name_one": "Sudden and violent",
            "seizure_name_two": "Super sciency name",
            "seizure_name_three": "",
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


class TestAdminIndex(TestCase):
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

    def test_admin_index_loads_if_user_logged_in(self):
        """ Tests whether the Admin Index page loads if the user is logged
         in."""

        test_user=models.User.objects.get(
            username="testuser"
        )

        self.client.force_login(test_user)

        response = self.client.get(reverse('index-private-admin'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_admin_index_redirects_if_user_not_logged_in(self):
        """ Tests whether the Admin Index page redirects to the login page if
         the user is not logged in."""

        response = self.client.get(reverse('index-private-admin'))

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
            allergies_conditions_that_exclude=False,
            heat_exhaustion_stroke=False,
            tetanus_shot_last_ten_years=True,
            seizures_last_six_monthes=False,
            doctor_concered_re_horse_activites=False,
            physical_or_mental_issues_affecting_riding=False,
            restriction_for_horse_activity_last_five_years=False,
            present_restrictions_for_horse_activity=False,
            limiting_surgeries_last_six_monthes=False,
            signature="TEST Oliver Queen",
            currently_taking_any_medication=False
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
            allergies_conditions_that_exclude=False,
            heat_exhaustion_stroke=False,
            tetanus_shot_last_ten_years=True,
            seizures_last_six_monthes=False,
            doctor_concered_re_horse_activites=False,
            physical_or_mental_issues_affecting_riding=False,
            restriction_for_horse_activity_last_five_years=False,
            present_restrictions_for_horse_activity=False,
            limiting_surgeries_last_six_monthes=False,
            signature="TEST Oliver Queen",
            currently_taking_any_medication=False
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
            "email":"Matt.Something@ftc.gov"
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

    def test_donation_adopt_horse_saves_with_valid_data_new_donor(self):

        form_data={
            "amount":"300",
            "name":"TEST New Donor",
            "email":"new@donor.com"
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

        session_goals=models.SessionGoals(
            participant_id=test_participant,
            session_id=session_plan,
            goal_type="S",
            goal_description="Some text",
            motivation="Don't die."
        )
        session_goals.save()

        horse_info=models.Horse(
            name="Charlie",
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
            date="2014-3-5",
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

    def test_session_plan_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Bobby Bobbers",
            "birth_date": "1986-7-21",
            "date": "2016-5-1",
            "horse_name": "Charlie",
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

    def test_session_plan_form_not_valid_participant_name(self):
        """ Verify that a Session Plan form view, populated with an invalid
         participant name, displays an error message. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST I'm Not Bobby Bobbers",
            "birth_date": "1986-7-21",
            "date": "2016-5-1",
            "horse_name": "Charlie",
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

    def test_session_plan_form_not_valid_birth_date(self):
        """ Verify that a Session Plan form view, populated with an invalid
         participant birth date, displays an error message. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Bobby Bobbers",
            "birth_date": "1900-0-01",
            "date": "2016-5-1",
            "horse_name": "Charlie",
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

    def test_session_plan_form_saves_with_valid_data(self):
        """ Verify that a Session Plan form view, populated with
         valid data, correctly saves the form to the database. """

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        form_data={
            "name": "TEST Bobby Bobbers",
            "birth_date": "1986-7-21",
            "date": "2016-5-1",
            "horse_name": "Charlie",
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

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-session-plan",
        kwargs={"participant_id",
        test_participant.participant_id}), form_data)

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
            print("Retrieving new SessionPlan record...")
            session_plan_in_db=(models.Session
                .objects.get(
                    participant_id=participant_in_db,
                    date=form_data["date"]
                )
            )
            print(
                "Successfully retrieved new SessionPlan record."
            )
        except:
            print(
                "ERROR: Unable to retreive new SessionPlan record!"
            )

        # Check that the attributes in the MediaRelease were set correctly:
        print(
            "Checking stored SessionPlan attributes..."
        )
        self.assertEqual(
            # Format the retrieved date so it matches the input format:
            "{d.year}-{d.month}-{d.day}".format(d=session_plan_in_db.date),
            form_data["date"]
        )

    def test_session_plan_form_with_invalid_participant_name(self):
        """ Verify that a Session Plan form view, populated with
         an invalid participant name, displays an error message. """

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        form_data={
            "name": "TEST I'm Not Bobby Bobbers",
            "birth_date": "1986-7-21",
            "date": "2016-5-1",
            "horse_name": "Charlie",
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

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-session-plan",
        kwargs={"participant_id",
        test_participant.participant_id}), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

    def test_media_release_form_with_invalid_participant_date(self):
        """ Verify that a Session Plan form view, populated with
         an invalid participant date, displays an error message. """

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        form_data={
            "name": "TEST Bobby Bobbers",
            "birth_date": "1900-1-02",
            "date": "2016-5-1",
            "horse_name": "Charlie",
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

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-session-plan",
        kwargs={"participant_id",
        test_participant.participant_id}), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_PARTICIPANT_NOT_FOUND
            )
        )

        form_data={
            "name": "TEST Bobby Bobbers sdfsdfslkfjslkjslgkjsdiogjsgiosjgsjgoijsgio",
            "birth_date": "Not A Date",
            "date": "2016-5-1",
            "horse_name": "Charlie",
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

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-session-plan",
        kwargs={"participant_id",
        test_participant.participant_id}), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertTrue(
            response.context["error_text"] == (
                views.ERROR_TEXT_FORM_INVALID
            )
        )

    def test_session_plan_form_with_duplicate_pk(self):
        """ Regresison test for Issue #47. The form should throw an error if the
         particpant already has a SessionPlan record with the same
         (participant_id, date) as its primary key. """

        test_participant=models.Participant.objects.get(
            name="TEST Bobby Bobbers",
            birth_date="1986-7-21"
        )

        form_data={
            "name": "TEST Bobby Bobbers",
            "birth_date": "1986-7-21",
            "date": "2016-5-1",
            "horse_name": "Charlie",
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

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("private-form-session-plan",
        kwargs={"participant_id",
        test_participant.participant_id}), form_data)

        # Assert that the reponse code is 200 (OK):
        self.assertEqual(response.status_code, 200)

        # Assert that the context for the new view contains the correct error:
        self.assertEqual(
            views.ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK.format(
                form="session plan"
            ),
            response.context["error_text"]
        )
