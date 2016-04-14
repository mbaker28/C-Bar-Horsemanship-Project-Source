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
        response = self.client.get(reverse('public-form-background'))
        self.assertEqual(response.status_code, 200) # Loaded...

    def test_seizure_form_loads(self):
        """ Tests whether the Seizure Evaluation form loads. """
        response = self.client.get(reverse('public-form-seizure'))
        self.assertEqual(response.status_code, 200) # Loaded...

class TestApplicationForm(TestCase):
    def setUp(self):
        setup_test_environment() #Initialize the test enviornment
        client=Client() #Make a test client (someone viewing the database)

    def test_application_form_creates_participant(self):
        """ Tests whether the form creates a participant record once all
            fields are entered. """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Matt Murdock",
            "birth_date": "1989-5-20",
            "email": "matt@nelsonandmurdock.com",
            "weight": "180.0",
            "gender": "M",
            "guardian_name": "Stick",
            "height": "69.0",
            "minor_status": "G",
            "address_street": "1234 Murdock Street",
            "address_city": "Hell's Kitchen",
            "address_zip": "654321",
            "phone_home": "(400) 100-200",
            "phone_cell": "(400) 200-300",
            "phone_work": "(400) 300-400",
            "school_institution": "Stick's School of Kung Fu"
        }
        form=forms.ApplicationForm(form_data)

        if form.is_valid(): # Performs validation, needed for form.cleaned_data
            print("Form is valid.")

            try:
                print("Searching database...")
                participant_instance=models.Participant.objects.get(
                    name=form.cleaned_data["name"],
                    birth_date=form.cleaned_data["birth_date"]
                )
                print("Participant already exists.")
                found_participant=True

            except ObjectDoesNotExist:
                found_participant=False

        else:
            print("Form is not valid.")

        # We should say we could find the participant:
        #self.assertEquals(found_participant, True)

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
            address_zip="424278",
            phone_home="(300) 200-100",
            phone_cell="(300) 500-600",
            phone_work="(598) 039-3008",
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
            address_zip="889922",
            phone_home="(300) 200-100",
            phone_cell="(300) 500-600",
            phone_work="(598) 039-3008",
        )
        test_participant_no_med_record.save()

        test_medical_info=models.MedicalInfo(
            participant_id=test_participant,
            date="2016-1-1",
            primary_physician_name="Dr. Default",
            primary_physician_phone="(111) 111-1111",
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

    def test_emergency_authorization_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Bruce Wayne",
            "birth_date": "1984-6-24",
            "primary_physician_name": "Dr. Buffalo Wings",
            "primary_physician_phone": "(111) 222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "(404) 333-9999",
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
            "primary_physician_phone": "(111) 222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "(404) 333-9999",
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
            "primary_physician_phone": "(111) 222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "(404) 333-9999",
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
            "primary_physician_phone": "(111) 222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "(404) 333-9999",
            "emerg_contact_relation": "Family Friend",
            "consents_emerg_med_treatment": "Y",
            "date": "2016-1-1",
            "signature": "TEST Bruce Wayne"
        }

        # Send a post request to the form view with the form_data defined above:
        response=self.client.post(reverse("public-form-emerg-auth"), form_data)

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
            "primary_physician_phone": "(111) 222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "(404) 333-9999",
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
            "primary_physician_phone": "(111) 222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "(404) 333-9999",
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
            "primary_physician_phone": "(111) 222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "(404) 333-9999",
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
            "primary_physician_phone": "(111) 222-3333",
            "pref_medical_facility": "Super Awesome Medical Facility",
            "insurance_provider": "Kinda Sketchy Insurance, Ltd.",
            "insurance_policy_num": "666FTC",
            "emerg_contact_name": "Lost Person",
            "emerg_contact_phone": "(404) 333-9999",
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
            address_zip="424278",
            phone_home="(300) 200-100",
            phone_cell="(300) 500-600",
            phone_work="(598) 039-3008",
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
            address_zip="889922",
            phone_home="(300) 200-100",
            phone_cell="(300) 500-600",
            phone_work="(598) 039-3008",
        )
        test_participant_no_med_record.save()

        test_medical_info=models.MedicalInfo(
            participant_id=test_participant,
            date="2016-1-1",
            primary_physician_name="Dr. Default",
            primary_physician_phone="(111) 111-1111",
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
            address_zip="424278",
            phone_home="(300) 200-100",
            phone_cell="(300) 500-600",
            school_institution="Ra's Al Ghul School of Ninjutsu"
        )
        test_participant.save()

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
            address_zip="424278",
            phone_home="(300) 200-100",
            phone_cell="(300) 500-600",
            school_institution="Ra's Al Ghul School of Ninjutsu"
        )
        test_participant.save()

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
            "medication_one_duration": "9 months",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_duration": "2012-now",
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
            "medication_one_duration": "9 months",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_duration": "2012-now",
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
            "medication_one_duration": "9 months",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_duration": "2012-now",
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
            "medication_one_duration": "9 months",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_duration": "2012-now",
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

        # DISABLED: We don't have a post form url redirect location or view yet
        # Assert the the redirect url matches the post-form page:
        # self.assertEqual(
        #     resp['Location'],
        #     'http://testserver/thank you place'
        # )

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
            "medication_one_duration": "9 months",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_duration": "2012-now",
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
            "medication_one_duration": "9 months",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_duration": "2012-now",
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
            "medication_one_duration": "9 months",
            "medication_one_frequency": "Every 6 hours",
            "medication_two_name": "Asprin",
            "medication_two_duration": "2012-now",
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
            address_zip="10018",
            phone_home="(123) 456-7890",
            phone_cell="(444) 393-0098",
            phone_work="(598) 039-3008",
            school_institution="SHIELD"
        )
        test_participant.save()

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
            address_zip="10018",
            phone_home="(123) 456-7890",
            phone_cell="(444) 393-0098",
            phone_work="(598) 039-3008",
            school_institution="SHIELD"
        )
        test_participant.save()

    def test_seizure_evaluation_form_finds_valid_participant(self):
        """ Tests whether the form finds a valid participant record if a
         matching (name, date) is entered """

        # If we are able to find the matching record, we set this to True:
        found_participant=False

        form_data={
            "name": "TEST Peter Parker",
            "birth_date": "1985-4-02",
            "date": "2016-03-31",
            "guardian_name": "Bob Burger",
            "phone_home": "(123) 123-4567",
            "phone_cell": "(321) 765-4321",
            "phone_work": "(987) 654-3210",
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
