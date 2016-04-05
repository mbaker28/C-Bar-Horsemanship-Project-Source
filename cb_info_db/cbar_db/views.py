from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import logging
from cbar_db import forms
from cbar_db import models

ERROR_TEXT_PARTICIPANT_NOT_FOUND=(
    "The requested participant isn't in the database."
)
ERROR_TEXT_PARTICIPANT_ALREADY_EXISTS=(
    "The participant already exists in the database."
)
ERROR_TEXT_MEDICAL_INFO_NOT_FOUND=(
    "The requested participant does not have their medical information on file."
    " Please fill out a medical release first."
)
ERROR_TEXT_FORM_INVALID=(
    "Error validating form."
)

loggeyMcLogging=logging.getLogger(__name__)

def index_public(request):
    """ Website index view. """
    return render(request, 'cbar_db/index.html')


def index_public_forms(request):
    """ Public forms index view. """
    return render(request, 'cbar_db/forms/public/public.html')


def public_form_application(request):
    """ Application form view. """

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form=forms.ApplicationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Create an instance of the ApplicationForm model to hold form data
            try:
                # Find the participant that matches the name and birth date from
                # the form data:
                participant=models.Participant.objects.get(
                    name=form.cleaned_data['name'],
                    birth_date=form.cleaned_data['birth_date']
                )
                return render(
                    request,
                    "cbar_db/forms/public/application.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_ALREADY_EXISTS,
                    }
                )

            except ObjectDoesNotExist:
                # Create a new ApplicationForm for the participant and save it:
                form_data_application=models.Participant(
                    participant_id=participant,
                    name=form.cleaned_data['name'],
                    birth_date=form.cleaned_data['birth_date'],
                    height=form.cleaned_data['height'],
                    weight=form.cleaned_data['weight'],
                    gender=form.cleaned_data['gender'],
                    minor_status=form.cleaned_data['minor_status'],
                    school_institution=form.cleaned_data['school_institution'],
                    guardian_name=form.cleaned_data['guardian_name'],
                    address_street=form.cleaned_data['address_street'],
                    address_city=form.cleaned_data['address_city'],
                    address_zip=form.cleaned_data['address_zip'],
                    phone_home=form.cleaned_data['phone_home'],
                    phone_cell_work=form.cleaned_data['phone_cell_work'],
                    email=form.cleaned_data['email'],
                    signature=form.cleaned_data['signature'],
                    date=form.cleaned_data['date']
                )
                form_data_application.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/')

        else:
            # The form is not valid.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/public/application.html",
                {
                    'form': form,
                    'error_text': ERROR_TEXT_FORM_INVALID,
                }
            )

    else:
        # If request type is GET (or any other method) create a blank form.
        form=forms.ApplicationForm()

        return render(
            request,
            'cbar_db/forms/public/application.html',
            {'form': form}
        )

def public_form_med_release(request):
    """ Medical Release form view. Handles viewing and saving the form.

    Viewing form (GET): Display the form
    Saving form (POST):
        -Do something
    """

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        # Create a form instance and populate it with data from the request:
        form=forms.MedicalReleaseForm(request.POST)

        # Check whether the form data entered is valid:
        if form.is_valid():
            loggeyMcLogging.error("The form is valid")
            # Find the participant's record based on their (name, birth_date):
            try:
                participant=models.Participant.objects.get(
                    name=form.cleaned_data['signature'],
                    birth_date=form.cleaned_data['birth_date']
                )
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/public/medical_release.html",
                    {
                        'form': form,
                        'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
                    }
                )

            medical_info=models.MedicalInfo(
                participant_id=participant,
                date=form.cleaned_data["date"],
                primary_physician_name=(
                    form.cleaned_data["primary_physician_name"]
                ),
                primary_physician_phone=(
                    form.cleaned_data["primary_physician_phone"]
                ),
                last_seen_by_physician_date=(
                    form.cleaned_data["last_seen_by_physician_date"]
                ),
                last_seen_by_physician_reason=(
                    form.cleaned_data["last_seen_by_physician_reason"]
                ),
                allergies_conditions_that_exclude=(
                    form.cleaned_data["allergies_conditions_that_exclude"]
                ),
                allergies_conditions_that_exclude_description=(
                    form.cleaned_data["allergies_conditions_that_exclude"
                        "_description"]
                ),
                heat_exhaustion_stroke=(
                    form.cleaned_data["heat_exhaustion_stroke"]
                ),
                tetanus_shot_last_ten_years=(
                    form.cleaned_data["tetanus_shot_last_ten_years"]
                ),
                seizures_last_six_monthes=(
                    form.cleaned_data["seizures_last_six_monthes"]
                ),
                currently_taking_any_medication=(
                    form.cleaned_data["currently_taking_any_medication"]
                ),
                doctor_concered_re_horse_activites=(
                    form.cleaned_data["doctor_concered_re_horse_activites"]
                ),
                physical_or_mental_issues_affecting_riding=(
                    form.cleaned_data["physical_or_mental_issues_affecting"
                        "_riding"]
                ),
                physical_or_mental_issues_affecting_riding_description=(
                    form.cleaned_data["physical_or_mental_issues_affecting"
                        "_riding_description"]
                ),
                restriction_for_horse_activity_last_five_years=(
                    form.cleaned_data["restriction_for_horse_activity_last"
                        "_five_years"]
                ),
                restriction_for_horse_activity_last_five_years_description=(
                    form.cleaned_data["restriction_for_horse_activity_last_five"
                        "_years_description"]
                ),
                present_restrictions_for_horse_activity=(
                    form.cleaned_data["present_restrictions_for_horse_activity"]
                ),
                limiting_surgeries_last_six_monthes=(
                    form.cleaned_data["limiting_surgeries_last_six_monthes"]
                ),
                signature=(form.cleaned_data["signature"])
            )
            medical_info.save()

            medication_one=models.Medication(
                medical_info_id=medical_info,
                medication_name=form.cleaned_data["medication_one_name"],
                duration_taken=form.cleaned_data["medication_one_duration"],
                frequency=form.cleaned_data["medication_one_frequency"]
            )
            medication_one.save()
            medication_two=models.Medication(
                medical_info_id=medical_info,
                medication_name=form.cleaned_data["medication_two_name"],
                duration_taken=form.cleaned_data["medication_two_duration"],
                frequency=form.cleaned_data["medication_two_frequency"]
            )
            medication_two.save()

            # Redirect to the home page:
            return HttpResponseRedirect('/')

        else:
            # The form is not valid
            loggeyMcLogging.error("The form is NOT valid")

            return render(
                request,
                "cbar_db/forms/public/medical_release.html",
                {
                    'form': form,
                    'error_text': ERROR_TEXT_FORM_INVALID,
                }
            )
    else:
        # If request type is GET (or any other method) create a blank form and
        # display it:
        form=forms.MedicalReleaseForm()
        return render(
            request,
            'cbar_db/forms/public/medical_release.html',
            {
                'form': form
            }
        )

def public_form_emerg_auth(request):
    """ Emegency Medical Treatment Authorization form view. Handles viewing and
     saving the form.

    Viewing form (GET): Display the form
    Saving form (POST):
        If participant exists:
            Update record in Participant
            Update record in MedicalInfo
            Create new record in AuthorizeEmergencyMedicalTreatment
        Else:
            Give an error
    """

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        # Create a form instance and populate it with data from the request:
        form=forms.EmergencyMedicalReleaseForm(request.POST)

        # Check whether the form data entered is valid:
        if form.is_valid():
            loggeyMcLogging.error("The form is valid")
            # Find the participant's record based on their (name, birth_date):
            try:
                participant=models.Participant.objects.get(
                    name=form.cleaned_data['name'],
                    birth_date=form.cleaned_data['birth_date']
                )
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/public/emergency_authorization.html",
                    {
                        'form': form,
                        'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
                    }
                )

            # If no exception, the participant exists. Update their records:
            try:
                # If the participant has a MedicalInfo record, retrieve it:
                medical_info=models.MedicalInfo.objects.get(
                    participant_id=participant
                )

                # Update the fields:
                medical_info.primary_physician_name=(
                    form.cleaned_data['primary_physician_name']
                )
                medical_info.primary_physician_phone=(
                    form.cleaned_data['primary_physician_phone']
                )

                # Save the updated record
                medical_info.save()
            except ObjectDoesNotExist:
                # The participant has no MedicalInfo record, prompt them to fill
                # out the Medical Release first.
                return render(
                    request,
                    "cbar_db/forms/public/emergency_authorization.html",
                    {
                        'form': form,
                        'error_text': (
                            ERROR_TEXT_MEDICAL_INFO_NOT_FOUND
                        ),
                    }
                )

            # Create a new AuthorizeEmergencyMedicalTreatment instance for the
            # participant and save it:
            authorize_emerg_medical=models.AuthorizeEmergencyMedicalTreatment(
                participant_id=participant,
                pref_medical_facility=(
                    form.cleaned_data['pref_medical_facility']
                ),
                insurance_provider=form.cleaned_data['insurance_provider'],
                insurance_policy_num=form.cleaned_data['insurance_policy_num'],
                emerg_contact_name=form.cleaned_data['emerg_contact_name'],
                emerg_contact_phone=form.cleaned_data['emerg_contact_phone'],
                emerg_contact_relation=(
                    form.cleaned_data['emerg_contact_relation']
                ),
                consents_emerg_med_treatment=(
                    form.cleaned_data['consents_emerg_med_treatment']
                ),
                date=form.cleaned_data['date'],
                signature=form.cleaned_data['signature']
            )
            authorize_emerg_medical.save()

            # Redirect to the home page:
            return HttpResponseRedirect('/')

        else:
            # The form is not valid
            loggeyMcLogging.error("The form is NOT valid")

            return render(
                request,
                "cbar_db/forms/public/emergency_authorization.html",
                {
                    'form': form,
                    'error_text': ERROR_TEXT_FORM_INVALID,
                }
            )

    else:
        # If request type is GET (or any other method) create a blank form.
        form=forms.EmergencyMedicalReleaseForm()

        return render(
            request,
            'cbar_db/forms/public/emergency_authorization.html',
            {
                'form': form,
            }
        )


def public_form_liability(request):
    """ Liability Release form view.

     If Participant exists:
        Create new instance of LiabilityReleaseForm and save it to the DB
    Else:
        Give an error
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form=forms.LiabilityReleaseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Create an instance of the LiabilityRelease model to hold form data
            try:
                # Find the participant that matches the name and birth date from
                # the form data:
                participant=models.Participant.objects.get(
                    name=form.cleaned_data['name'],
                    birth_date=form.cleaned_data['birth_date']
                )

            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/public/liability.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                    }
                )

            # Create a new LiabilityRelease for the participant and save it:
            form_data_liability=models.LiabilityRelease(
                participant_id=participant,
                signature=form.cleaned_data['signature'],
                date=form.cleaned_data['date']
            )
            form_data_liability.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/')

        else:
            # The form is not valid.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/public/liability.html",
                {
                    'form': form,
                    'error_text': ERROR_TEXT_FORM_INVALID,
                }
            )

    else:
        # If request type is GET (or any other method) create a blank form.
        form=forms.LiabilityReleaseForm()

        return render(
            request,
            'cbar_db/forms/public/liability.html',
            {'form': form}
        )

def public_form_media(request):
    """ Media Release form view.

    If Participant exists:
        Create new instance of MediaReleaseForm and save it to the DB
    Else:
        Give an error
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form=forms.MediaReleaseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Create an instance of the MediaRelease model to hold form data
            try:
                # Find the participant that matches the name and birth date from
                # the form data:
                participant=models.Participant.objects.get(
                    name=form.cleaned_data['name'],
                    birth_date=form.cleaned_data['birth_date']
                )

            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/public/media.html",
                    {
                        'form': form,
                        'error_text': ("The requested participant isn't in the"
                        " database."),
                    }
                )

            # Create a new MediaRelease for the participant and save it:
            form_data_media=models.MediaRelease(
                participant_id=participant,
                consent=form.cleaned_data['consent'],
                signature=form.cleaned_data['signature'],
                date=form.cleaned_data['date']
            )
            form_data_media.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/')

        else:
            # The form is not valid.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/public/media.html",
                {
                    'form': form,
                    'error_text': "Error validating form.",
                }
            )

    else:
        # If request type is GET (or any other method) create a blank form.
        form=forms.MediaReleaseForm()

        return render(
            request,
            'cbar_db/forms/public/media.html',
            {'form': form}
        )


def public_form_background(request):
    """ Background Check Authorization form view. """
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        form=forms.BackgroundCheckForm(request.POST)

        if form.is_valid():
            loggeyMcLogging.error("The form is valid")
            try:
                participant=models.Participant.objects.get(
                    name=form.cleaned_data['name'],
                    birth_date=form.cleaned_data['birth_date']
                )
            except ObjectDoesNotExist:
                return render(
                    request,
                    "cbar_db/forms/public/background.html",
                    {
                        'form': form,
                        'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
                    }
                )

            public_form_background=models.BackgroundCheck(
                participant_id=participant,
                date=form.cleaned_data['date'],
                signature=form.cleaned_data['signature'],
                driver_license_num=form.cleaned_data['driver_license_num']
            )
            public_form_background.save()

            # Redirect to the home page:
            return HttpResponseRedirect('/')

        else:
            form=forms.BackgroundCheckForm()
            return render(
                request,
                'cbar_db/forms/public/background.html',
                {
                    'form': form,
                    'error_text':ERROR_TEXT_FORM_INVALID,
                }
            )
    else:
        form=forms.BackgroundCheckForm()

        return render (
            request,
            'cbar_db/forms/public/background.html',
            {
                'form':form,
            }
        )

def public_form_seizure(request):
    """ Seizure Evaluation form view. """
    return render(request, 'cbar_db/forms/public/seizure.html')
