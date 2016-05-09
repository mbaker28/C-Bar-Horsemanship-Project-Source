from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
import logging
import time
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
ERROR_TEXT_INVALID_DATE=(
    "The requested date is not valid"
)
ERROR_TEXT_MEDIA_RELEASE_NOT_AVAILABLE=(
    "The Media Release requested is not available"
)
ERROR_TEXT_EMERG_AUTH_NOT_AVAILABLE=(
    "The requested Emergency Medical Treatment Authorization is not available."
)
ERROR_TEXT_LIABILITY_RELEASE_NOT_AVAILABLE=(
    "The Liability Release requested is not available."
)
ERROR_TEXT_BACKGROUND_CHECK_NOT_AVAILABLE=(
    "The Background Check Authorization requested is not available."
)
ERROR_TEXT_SEIZURE_EVAL_NOT_AVAILABLE=(
    "The Seizure Evaluation requested is not available."
)
ERROR_TEXT_DB_INTEGRITY=(
    "An internal database error has occured and the form could not be saved."
    " Please verify that you have not already filled out a form for this"
    " participant and date."
)
ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK=(
    "This participant already has a(n) {form} filed for this date."
    " You cannot have more than one {form} filed for the same date."
)

loggeyMcLogging=logging.getLogger(__name__)

def index_public(request):
    """ Website index view. """
    return render(request, 'cbar_db/index.html')

def index_public_forms(request):
    """ Public forms index view. """
    return render(request, 'cbar_db/forms/public/public.html')

def form_saved(request):
    """ Used to tell the user their form saved. """

    # Check if the user just typed the url in the menu bar:
    if request.GET.get("a") == "a":
        # The user was redirected here from a form, display the message:
        return render(request, "cbar_db/forms/form_saved.html")
    else:
        # The user just typed in the address, redirect to the home page:
        return HttpResponseRedirect("/")

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
                # Calculate the height in inches
                height_in_inches=(
                    (form.cleaned_data["height_feet"]*12)
                    + form.cleaned_data["height_inches"]
                )

                # Create a new ApplicationForm for the participant and save it:
                form_data_application=models.Participant(
                    name=form.cleaned_data['name'],
                    birth_date=form.cleaned_data['birth_date'],
                    height=height_in_inches,
                    weight=form.cleaned_data['weight'],
                    gender=form.cleaned_data['gender'],
                    minor_status=form.cleaned_data['minor_status'],
                    school_institution=form.cleaned_data['school_institution'],
                    guardian_name=form.cleaned_data['guardian_name'],
                    address_street=form.cleaned_data['address_street'],
                    address_city=form.cleaned_data['address_city'],
                    address_state=form.cleaned_data['address_state'],
                    address_zip=form.cleaned_data['address_zip'],
                    phone_home=form.cleaned_data['phone_home'],
                    phone_cell=form.cleaned_data['phone_cell'],
                    phone_work=form.cleaned_data['phone_work'],
                    email=form.cleaned_data['email'],
                )
                form_data_application.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

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
    """ Medical Release form view. Handles viewing and saving the form. """

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
                    name=form.cleaned_data['name'],
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

            try:
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
                    signature=(form.cleaned_data["signature"]),
                    pregnant=form.cleaned_data["pregnant"],
                )
                medical_info.save()
            # Catch duplicate composite primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/public/medical_release.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="health information record")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/public/medical_release.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            if form.cleaned_data["medication_one_name"] != "":
                medication_one=models.Medication(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    medication_name=form.cleaned_data["medication_one_name"],
                    reason_taken=form.cleaned_data["medication_one_reason"],
                    frequency=form.cleaned_data["medication_one_frequency"]
                )
                medication_one.save()
            if form.cleaned_data["medication_two_name"] != "":
                medication_two=models.Medication(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    medication_name=form.cleaned_data["medication_two_name"],
                    reason_taken=form.cleaned_data["medication_two_reason"],
                    frequency=form.cleaned_data["medication_two_frequency"]
                )
                medication_two.save()

            # Redirect to the home page:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

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
            Create new record in MedicalInfo with old & updated information
            Create copies of Medication records linked with old MedicalInfo
                Update their dates to match updated MedicalInfo
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
                # If the participant has a MedicalInfo record,
                # retrieve the most recent one:
                medical_info=models.MedicalInfo.objects.filter(
                    participant_id=participant
                ).latest("date")

                # Create a new copy of medications from the old MedicalInfo
                # record and update their dates so that they will link to the
                # current medical_info record:
                medications=models.Medication.objects.filter(
                    date=medical_info.date,
                    participant_id=participant
                )
                for medication in medications:
                    medication.pk=None
                    medication.date=form.cleaned_data["date"]
                    medication.save()

                medical_info.pk=None # PK=none -> .save() makes a new copy

                # Update the fields:
                medical_info.primary_physician_name=(
                    form.cleaned_data['primary_physician_name']
                )
                medical_info.primary_physician_phone=(
                    form.cleaned_data['primary_physician_phone']
                )
                medical_info.date=(
                    form.cleaned_data["date"]
                )

                # Save the new, updated record
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
            # Catch duplicate composite primary keys:
            except IntegrityError as error: # pragma: no cover
                # Excluded from coverage reports because I know it's getting run
                # and the tests are correctly verifying manually observed
                # behaviour. -Michael

                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/public/emergency_authorization.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form=(
                                    "emergency medical treatment authorization")
                                )
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/public/emergency_authorization.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # Create a new AuthorizeEmergencyMedicalTreatment instance for the
            # participant and save it:
            try:
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
            # Catch duplicate composite primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/public/emergency_authorization.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form=(
                                    "emergency medical treatment authorization")
                                )
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/public/emergency_authorization.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # Redirect to the home page:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

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
            try:
                form_data_liability=models.LiabilityRelease(
                    participant_id=participant,
                    signature=form.cleaned_data['signature'],
                    date=form.cleaned_data['date']
                )
                form_data_liability.save()
            # Catch duplicate composite primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/public/liability.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="liability release")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/public/liability.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

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

    If Participant exists and duplicate form not found:
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

            try:
                # Create a new MediaRelease for the participant and save it:
                form_data_media=models.MediaRelease(
                    participant_id=participant,
                    consent=form.cleaned_data['consent'],
                    signature=form.cleaned_data['signature'],
                    date=form.cleaned_data['date']
                )
                form_data_media.save()
            # Catch duplicate composite primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/public/media.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="media release")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/public/media.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

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

            try:
                public_form_background=models.BackgroundCheck(
                    participant_id=participant,
                    date=form.cleaned_data['date'],
                    signature=form.cleaned_data['signature'],
                    driver_license_num=form.cleaned_data['driver_license_num']
                )
                public_form_background.save()
            # Catch duplicate composite primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/public/background.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="background check authorization")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/public/background.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # Redirect to the home page:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

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

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form=forms.SeizureEvaluationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Create an instance of the SeizureEval model to hold form data
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
                    "cbar_db/forms/public/seizure.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND
                    }
                )

            # Update the participant's Participant record and save it:
            participant.phone_home=form.cleaned_data["phone_home"]
            participant.phone_cell=form.cleaned_data["phone_cell"]
            participant.phone_work=form.cleaned_data["phone_work"]
            participant.guardian_name=form.cleaned_data["guardian_name"]
            participant.save()

            # Create a new SeizureEval for the participant and save it:
            try:
                seizure_data=models.SeizureEval(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    date_of_last_seizure=form.cleaned_data["date_of_last_seizure"],
                    seizure_frequency=form.cleaned_data["seizure_frequency"],
                    duration_of_last_seizure=form.cleaned_data["duration_of_last_seizure"],
                    typical_cause=form.cleaned_data["typical_cause"],
                    seizure_indicators=form.cleaned_data["seizure_indicators"],
                    after_effect=form.cleaned_data["after_effect"],
                    during_seizure_stare=form.cleaned_data["during_seizure_stare"],
                    during_seizure_stare_length=form.cleaned_data["during_seizure_stare_length"],
                    during_seizure_walks=form.cleaned_data["during_seizure_walks"],
                    during_seizure_aimless=form.cleaned_data["during_seizure_aimless"],
                    during_seizure_cry_etc=form.cleaned_data["during_seizure_cry_etc"],
                    during_seizure_bladder_bowel=form.cleaned_data["during_seizure_bladder_bowel"],
                    during_seizure_confused_etc=form.cleaned_data["during_seizure_confused_etc"],
                    during_seizure_other=form.cleaned_data["during_seizure_other"],
                    during_seizure_other_description=form.cleaned_data["during_seizure_other_description"],
                    knows_when_will_occur=form.cleaned_data["knows_when_will_occur"],
                    can_communicate_when_will_occur=form.cleaned_data["can_communicate_when_will_occur"],
                    action_to_take_dismount=form.cleaned_data["action_to_take_dismount"],
                    action_to_take_send_note=form.cleaned_data["action_to_take_send_note"],
                    action_to_take_do_nothing=form.cleaned_data["action_to_take_do_nothing"],
                    action_to_take_allow_time=form.cleaned_data["action_to_take_allow_time"],
                    action_to_take_allow_time_how_long=form.cleaned_data["action_to_take_allow_time_how_long"],
                    action_to_take_report_immediately=form.cleaned_data["action_to_take_report_immediately"],
                    signature=form.cleaned_data["signature"],
                    type_of_seizure=form.cleaned_data["type_of_seizure"],
                )
                seizure_data.save()
            # Catch duplicate composite primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/public/seizure.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="seizure evaluation")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/public/seizure.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            if form.cleaned_data["medication_one_name"] != "":
                medication_one=models.Medication(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    medication_name=form.cleaned_data["medication_one_name"],
                    reason_taken=form.cleaned_data["medication_one_reason"],
                    frequency=form.cleaned_data["medication_one_frequency"]
                )
                medication_one.save()

            if form.cleaned_data["medication_two_name"] != "":
                medication_two=models.Medication(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    medication_name=form.cleaned_data["medication_two_name"],
                    reason_taken=form.cleaned_data["medication_two_reason"],
                    frequency=form.cleaned_data["medication_two_frequency"]
                )
                medication_two.save()

            if form.cleaned_data["medication_three_name"] != "":
                medication_three=models.Medication(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    medication_name=form.cleaned_data["medication_three_name"],
                    reason_taken=form.cleaned_data["medication_three_reason"],
                    frequency=form.cleaned_data["medication_three_frequency"]
                )
                medication_three.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

        else:
            # The form is not valid.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/public/seizure.html",
                {
                    'form': form,
                    'error_text': ERROR_TEXT_FORM_INVALID
                }
            )

    else:
        # If request type is GET (or any other method) create a blank form.
        form=forms.SeizureEvaluationForm()

        return render(
            request,
            'cbar_db/forms/public/seizure.html',
            {
                'form': form
            }
        )

def donation_index(request):
    """ Index for donations view. """
    return render(request, 'cbar_db/forms/donation/donation_index.html')

def donation_participant(request):
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        form=forms.ParticipantAdoptionForm(request.POST)

        if form.is_valid():
            loggeyMcLogging.error("The form is valid")

            try:
                # Stupid gay shit..
                loggeyMcLogging.error("Seaching for existing donor...")
                donor=models.objects.Donor.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"]
                )
                loggeyMcLogging.error("Existing donor found.")
            except:
                # More stupid gay shit...
                loggeyMcLogging.error(
                    "Existing donor not found. Creating new donor..."
                )
                donor=models.Donor(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"]
                )
                donor.save()

            donation=models.Donation(
                donor_id=donor,
                donation_type=models.Donation.DONATION_ADOPT_PARTICIPANT,
                amount=form.cleaned_data["amount"]
            )
            donation.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/')

        else:
            loggeyMcLogging.error("The form is NOT Valid")
            return render(
                request,
                'cbar_db/forms/donation/donation_participant.html',
                {
                    'form': form,
                    'error_text': ERROR_TEXT_FORM_INVALID
            }
        )

    else:
        form=forms.ParticipantAdoptionForm()
        return render(
            request,
            'cbar_db/forms/donation/donation_participant.html',
            {
                'form': form
            }
        )

def donation_horse(request):
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        form=forms.HorseAdoptionForm(request.POST)

        if form.is_valid():
            loggeyMcLogging.error("The form is valid")

            try:
                loggeyMcLogging.error("Searching for existing donor record...")
                donor=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"]
                )
                loggeyMcLogging.error("Found existing donor record.")
            except:
                loggeyMcLogging.error(
                    "Existing donor record not found. Creating new record..."
                )
                donor=models.Donor(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"]
                )
                donor.save()

            donation=models.Donation(
                donor_id=donor,
                donation_type=models.Donation.DONATION_ADOPT_HORSE,
                amount=(
                    form.cleaned_data["amount"]
                )
            )
            donation.save()

            # Redirect to the home page:
            return HttpResponseRedirect("/")

        else:
            loggeyMcLogging.error("The form is NOT Valid")
            return render(
                request,
                'cbar_db/forms/donation/donation_horse.html',
                {
                    'form': form,
                    'error_text': ERROR_TEXT_FORM_INVALID
                }
            )

    else:
        form=forms.HorseAdoptionForm()
        return render(
            request,
            'cbar_db/forms/donation/donation_horse.html',
            {
                'form': form
            }
        )

def donation_monetary(request):
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        form=forms.MonetaryDonationForm(request.POST)

        if form.is_valid():
            loggeyMcLogging.error("The form is valid")

            try:
                donor=models.Donor.objects.get(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"]
                )
            except ObjectDoesNotExist:
                donor=models.Donor(
                    name=form.cleaned_data["name"],
                    email=form.cleaned_data["email"]
                )
                donor.save()

            donation=models.Donation(
                donor_id=donor,
                donation_type=models.Donation.DONATION_MONETARY,
                amount=form.cleaned_data["amount"],
                purpose=form.cleaned_data["purpose"]
            )
            donation.save()

            # Redirect to a new page
            return HttpResponseRedirect("/")

        else:
            loggeyMcLogging.error("The form is NOT Valid")
            return render(
                request,
                'cbar_db/forms/donation/donation_monetary.html',
                {
                    'form': form,
                    'error_text': ERROR_TEXT_FORM_INVALID
            }
        )

    else:
        form=forms.MonetaryDonationForm()
        return render(
            request,
            'cbar_db/forms/donation/donation_monetary.html',
            {
                'form': form
            }
        )


@login_required
def private_form_rider_eval_checklist(request, participant_id):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form=forms.RiderEvalChecklistForm(request.POST)

        # Retrieve the Participant record bassed on the participant_id passed
        # via the URL:
        try:
            participant=models.Participant.objects.get(
                participant_id=participant_id
            )
        except ObjectDoesNotExist:
            # The participant doesn't exist.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/private/rider_eval_checklist_form.html",
                {
                    'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                }
            )

        # check whether it's valid:
        if form.is_valid():
            try:
                form_data_rider_eval_checklist=models.EvalRidingExercises(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    comments=form.cleaned_data["comments"],
                    basic_trail_rules=form.cleaned_data["basic_trail_rules"],
                    mount=form.cleaned_data["mount"],
                    dismount=form.cleaned_data["dismount"],
                    emergency_dismount=form.cleaned_data["emergency_dismount"],
                    four_natural_aids=form.cleaned_data["four_natural_aids"],
                    basic_control=form.cleaned_data["basic_control"],
                    reverse_at_walk=form.cleaned_data["reverse_at_walk"],
                    reverse_at_trot=form.cleaned_data["reverse_at_trot"],
                    never_ridden=form.cleaned_data["never_ridden"],
                    seat_at_walk=form.cleaned_data["seat_at_walk"],
                    seat_at_trot=form.cleaned_data["seat_at_trot"],
                    seat_at_canter=form.cleaned_data["seat_at_canter"],
                    basic_seat_english=form.cleaned_data["basic_seat_english"],
                    basic_seat_western=form.cleaned_data["basic_seat_western"],
                    hand_pos_english=form.cleaned_data["hand_pos_english"],
                    hand_post_western=form.cleaned_data["hand_post_western"],
                    two_point_trot=form.cleaned_data["two_point_trot"],
                    circle_trot_no_stirrups=(
                        form.cleaned_data["circle_trot_no_stirrups"]
                    ),
                    circle_at_canter=form.cleaned_data["circle_at_canter"],
                    circle_canter_no_stirrups=(
                        form.cleaned_data["circle_canter_no_stirrups"]
                    ),
                    two_point_canter=form.cleaned_data["two_point_canter"],
                    circle_at_walk=form.cleaned_data["circle_at_walk"],
                    circle_at_trot=form.cleaned_data["circle_at_trot"],
                    holds_handhold_walk=(
                        form.cleaned_data["holds_handhold_walk"]
                    ),
                    holds_handhold_sit_trot=(
                        form.cleaned_data["holds_handhold_sit_trot"]
                    ),
                    holds_handhold_post_trot=(
                        form.cleaned_data["holds_handhold_post_trot"]
                    ),
                    holds_handhold_canter=(
                        form.cleaned_data["holds_handhold_canter"]
                    ),
                    holds_reins_walk=form.cleaned_data["holds_reins_walk"],
                    holds_reins_sit_trot=(
                        form.cleaned_data["holds_reins_sit_trot"]
                    ),
                    holds_reins_post_trot=(
                        form.cleaned_data["holds_reins_post_trot"]
                    ),
                    holds_reins_canter=form.cleaned_data["holds_reins_canter"],
                    shorten_lengthen_reins_walk=(
                        form.cleaned_data["shorten_lengthen_reins_walk"]
                    ),
                    shorten_lengthen_reins_sit_trot=(
                        form.cleaned_data["shorten_lengthen_reins_sit_trot"]
                    ),
                    shorten_lengthen_reins_post_trot=(
                        form.cleaned_data["shorten_lengthen_reins_post_trot"]
                    ),
                    shorten_lengthen_reins_canter=(
                        form.cleaned_data["shorten_lengthen_reins_canter"]
                    ),
                    can_control_horse_walk=(
                        form.cleaned_data["can_control_horse_walk"]
                    ),
                    can_control_horse_sit_trot=(
                        form.cleaned_data["can_control_horse_sit_trot"]
                    ),
                    can_control_horse_post_trot=(
                        form.cleaned_data["can_control_horse_post_trot"]
                    ),
                    can_control_horse_canter=(
                        form.cleaned_data["can_control_horse_canter"]
                    ),
                    can_halt_walk=(
                        form.cleaned_data["can_halt_walk"]
                    ),
                    can_halt_sit_trot=(
                        form.cleaned_data["can_halt_sit_trot"]
                    ),
                    can_halt_post_trot=(
                        form.cleaned_data["can_halt_post_trot"]
                    ),
                    can_halt_canter=(
                        form.cleaned_data["can_halt_canter"]
                    ),
                    drop_pickup_stirrups_walk=(
                        form.cleaned_data["drop_pickup_stirrups_walk"]
                    ),
                    drop_pickup_stirrups_sit_trot=(
                        form.cleaned_data["drop_pickup_stirrups_sit_trot"]
                    ),
                    drop_pickup_stirrups_post_trot=(
                        form.cleaned_data["drop_pickup_stirrups_post_trot"]
                    ),
                    drop_pickup_stirrups_canter=(
                        form.cleaned_data["drop_pickup_stirrups_canter"]
                    ),
                    rides_no_stirrups_walk=(
                        form.cleaned_data["rides_no_stirrups_walk"]
                    ),
                    rides_no_stirrups_sit_trot=(
                        form.cleaned_data["rides_no_stirrups_sit_trot"]
                    ),
                    rides_no_stirrups_post_trot=(
                        form.cleaned_data["rides_no_stirrups_post_trot"]
                    ),
                    rides_no_stirrups_canter=(
                        form.cleaned_data["rides_no_stirrups_canter"]
                    ),
                    maintain_half_seat_walk=(
                        form.cleaned_data["maintain_half_seat_walk"]
                    ),
                    maintain_half_seat_sit_trot=(
                        form.cleaned_data["maintain_half_seat_sit_trot"]
                    ),
                    maintain_half_seat_post_trot=(
                        form.cleaned_data["maintain_half_seat_post_trot"]
                    ),
                    maintain_half_seat_canter=(
                        form.cleaned_data["maintain_half_seat_canter"]
                    ),
                    can_post_walk=(
                        form.cleaned_data["can_post_walk"]
                    ),
                    can_post_sit_trot=(
                        form.cleaned_data["can_post_sit_trot"]
                    ),
                    can_post_post_trot=(
                        form.cleaned_data["can_post_post_trot"]
                    ),
                    can_post_canter=(
                        form.cleaned_data["can_post_canter"]
                    ),
                    proper_diagonal_walk=(
                        form.cleaned_data["proper_diagonal_walk"]
                    ),
                    proper_diagonal_sit_trot=(
                        form.cleaned_data["proper_diagonal_sit_trot"]
                    ),
                    proper_diagonal_post_trot=(
                        form.cleaned_data["proper_diagonal_post_trot"]
                    ),
                    proper_diagonal_canter=(
                        form.cleaned_data["proper_diagonal_canter"]
                    ),
                    proper_lead_canter_sees=(
                        form.cleaned_data["proper_lead_canter_sees"]
                    ),
                    proper_lead_canter_knows=(
                        form.cleaned_data["proper_lead_canter_knows"]
                    ),
                    can_steer_over_cavalletti_walk=(
                        form.cleaned_data["can_steer_over_cavalletti_walk"]
                    ),
                    can_steer_over_cavalletti_sit_trot=(
                        form.cleaned_data["can_steer_over_cavalletti_sit_trot"]
                    ),
                    can_steer_over_cavalletti_post_trot=(
                        form.cleaned_data["can_steer_over_cavalletti_post_trot"]
                    ),
                    can_steer_over_cavalletti_canter=(
                        form.cleaned_data["can_steer_over_cavalletti_canter"]
                    ),
                    jump_crossbar_walk=(
                        form.cleaned_data["jump_crossbar_walk"]
                    ),
                    jump_crossbar_sit_trot=(
                        form.cleaned_data["jump_crossbar_sit_trot"]
                    ),
                    jump_crossbar_post_trot=(
                        form.cleaned_data["jump_crossbar_post_trot"]
                    ),
                    jump_crossbar_canter=(
                        form.cleaned_data["jump_crossbar_canter"]
                    ),
                    basic_trail_rules_com=(
                        form.cleaned_data["basic_trail_rules_com"]
                    ),
                    mount_com=(
                        form.cleaned_data["mount_com"]
                    ),
                    dismount_com=(
                        form.cleaned_data["dismount_com"]
                    ),
                    emergency_dismount_com=(
                        form.cleaned_data["emergency_dismount_com"]
                    ),
                    four_natural_aids_com=(
                        form.cleaned_data["four_natural_aids_com"]
                    ),
                    basic_control_com=(
                        form.cleaned_data["basic_control_com"]
                    ),
                    reverse_at_walk_com=(
                        form.cleaned_data["reverse_at_walk_com"]
                    ),
                    reverse_at_trot_com=(
                        form.cleaned_data["reverse_at_trot_com"]
                    ),
                    never_ridden_com=(
                        form.cleaned_data["never_ridden_com"]
                    ),
                    seat_at_walk_com=(
                        form.cleaned_data["seat_at_walk_com"]
                    ),
                    seat_at_trot_com=(
                        form.cleaned_data["seat_at_trot_com"]
                    ),
                    seat_at_canter_com=(
                        form.cleaned_data["seat_at_canter_com"]
                    ),
                    basic_seat_english_com=(
                        form.cleaned_data["basic_seat_english_com"]
                    ),
                    basic_seat_western_com=(
                        form.cleaned_data["basic_seat_western_com"]
                    ),
                    hand_pos_english_com=(
                        form.cleaned_data["hand_pos_english_com"]
                    ),
                    hand_post_western_com=(
                        form.cleaned_data["hand_post_western_com"]
                    ),
                    two_point_trot_com=(
                        form.cleaned_data["two_point_trot_com"]
                    ),
                    circle_trot_no_stirrups_com=(
                        form.cleaned_data["circle_trot_no_stirrups_com"]
                    ),
                    circle_at_canter_com=(
                        form.cleaned_data["circle_at_canter_com"]
                    ),
                    circle_canter_no_stirrups_com=(
                        form.cleaned_data["circle_canter_no_stirrups_com"]
                    ),
                    two_point_canter_com=(
                        form.cleaned_data["two_point_canter_com"]
                    ),
                    circle_at_walk_com=(
                        form.cleaned_data["circle_at_walk_com"]
                    ),
                    circle_at_trot_com=(
                        form.cleaned_data["circle_at_trot_com"]
                    ),
                    holds_handhold_walk_com=(
                        form.cleaned_data["holds_handhold_walk_com"]
                    ),
                    holds_handhold_sit_trot_com=(
                        form.cleaned_data["holds_handhold_sit_trot_com"]
                    ),
                    holds_handhold_post_trot_com=(
                        form.cleaned_data["holds_handhold_post_trot_com"]
                    ),
                    holds_handhold_canter_com=(
                        form.cleaned_data["holds_handhold_canter_com"]
                    ),
                    holds_reins_walk_com=(
                        form.cleaned_data["holds_reins_walk_com"]
                    ),
                    holds_reins_sit_trot_com=(
                        form.cleaned_data["holds_reins_sit_trot_com"]
                    ),
                    holds_reins_post_trot_com=(
                        form.cleaned_data["holds_reins_post_trot_com"]
                    ),
                    holds_reins_canter_com=(
                        form.cleaned_data["holds_reins_canter_com"]
                    ),
                    shorten_lengthen_reins_walk_com=(
                        form.cleaned_data["shorten_lengthen_reins_walk_com"]
                    ),
                    shorten_lengthen_reins_sit_trot_com=(
                        form.cleaned_data["shorten_lengthen_reins_sit_trot_com"]
                    ),
                    shorten_lengthen_reins_post_trot_com=(
                        form.cleaned_data["shorten_lengthen_reins_post_"
                            "trot_com"]
                    ),
                    shorten_lengthen_reins_canter_com=(
                        form.cleaned_data["shorten_lengthen_reins_canter_com"]
                    ),
                    can_control_horse_walk_com=(
                        form.cleaned_data["can_control_horse_walk_com"]
                    ),
                    can_control_horse_sit_trot_com=(
                        form.cleaned_data["can_control_horse_sit_trot_com"]
                    ),
                    can_control_horse_post_trot_com=(
                        form.cleaned_data["can_control_horse_post_trot_com"]
                    ),
                    can_control_horse_canter_com=(
                        form.cleaned_data["can_control_horse_canter_com"]
                    ),
                    can_halt_walk_com=(
                        form.cleaned_data["can_halt_walk_com"]
                    ),
                    can_halt_sit_trot_com=(
                        form.cleaned_data["can_halt_sit_trot_com"]
                    ),
                    can_halt_post_trot_com=(
                        form.cleaned_data["can_halt_post_trot_com"]
                    ),
                    can_halt_canter_com=(
                        form.cleaned_data["can_halt_canter_com"]
                    ),
                    drop_pickup_stirrups_walk_com=(
                        form.cleaned_data["drop_pickup_stirrups_walk_com"]
                    ),
                    drop_pickup_stirrups_sit_trot_com=(
                        form.cleaned_data["drop_pickup_stirrups_sit_trot_com"]
                    ),
                    drop_pickup_stirrups_post_trot_com=(
                        form.cleaned_data["drop_pickup_stirrups_post_trot_com"]
                    ),
                    drop_pickup_stirrups_canter_com=(
                        form.cleaned_data["drop_pickup_stirrups_canter_com"]
                    ),
                    rides_no_stirrups_walk_com=(
                        form.cleaned_data["rides_no_stirrups_walk_com"]
                    ),
                    rides_no_stirrups_sit_trot_com=(
                        form.cleaned_data["rides_no_stirrups_sit_trot_com"]
                    ),
                    rides_no_stirrups_post_trot_com=(
                        form.cleaned_data["rides_no_stirrups_post_trot_com"]
                    ),
                    rides_no_stirrups_canter_com=(
                        form.cleaned_data["rides_no_stirrups_canter_com"]
                    ),
                    maintain_half_seat_walk_com=(
                        form.cleaned_data["maintain_half_seat_walk_com"]
                    ),
                    maintain_half_seat_sit_trot_com=(
                        form.cleaned_data["maintain_half_seat_sit_trot_com"]
                    ),
                    maintain_half_seat_post_trot_com=(
                        form.cleaned_data["maintain_half_seat_post_trot_com"]
                    ),
                    maintain_half_seat_canter_com=(
                        form.cleaned_data["maintain_half_seat_canter_com"]
                    ),
                    can_post_walk_com=(
                        form.cleaned_data["can_post_walk_com"]
                    ),
                    can_post_sit_trot_com=(
                        form.cleaned_data["can_post_sit_trot_com"]
                    ),
                    can_post_post_trot_com=(
                        form.cleaned_data["can_post_post_trot_com"]
                    ),
                    can_post_canter_com=(
                        form.cleaned_data["can_post_canter_com"]
                    ),
                    proper_diagonal_walk_com=(
                        form.cleaned_data["proper_diagonal_walk_com"]
                    ),
                    proper_diagonal_sit_trot_com=(
                        form.cleaned_data["proper_diagonal_sit_trot_com"]
                    ),
                    proper_diagonal_post_trot_com=(
                        form.cleaned_data["proper_diagonal_post_trot_com"]
                    ),
                    proper_diagonal_canter_com=(
                        form.cleaned_data["proper_diagonal_canter_com"]
                    ),
                    proper_lead_canter_sees_com=(
                        form.cleaned_data["proper_lead_canter_sees_com"]
                    ),
                    proper_lead_canter_knows_com=(
                        form.cleaned_data["proper_lead_canter_knows_com"]
                    ),
                    can_steer_over_cavalletti_walk_com=(
                        form.cleaned_data["can_steer_over_cavalletti_walk_com"]
                    ),
                    can_steer_over_cavalletti_sit_trot_com=(
                        form.cleaned_data["can_steer_over_cavalletti_sit_"
                            "trot_com"]
                    ),
                    can_steer_over_cavalletti_post_trot_com=(
                        form.cleaned_data["can_steer_over_cavalletti_post_"
                            "trot_com"]
                    ),
                    can_steer_over_cavalletti_canter_com=(
                        form.cleaned_data["can_steer_over_cavalletti_"
                            "canter_com"]
                    ),
                    jump_crossbar_walk_com=(
                        form.cleaned_data["jump_crossbar_walk_com"]
                    ),
                    jump_crossbar_sit_trot_com=(
                        form.cleaned_data["jump_crossbar_sit_trot_com"]
                    ),
                    jump_crossbar_post_trot_com=(
                        form.cleaned_data["jump_crossbar_post_trot_com"]
                    ),
                    jump_crossbar_canter_com=(
                        form.cleaned_data["jump_crossbar_canter_com"]
                    )
                )
                form_data_rider_eval_checklist.save()


            # Catch duplicate composite primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if ("Duplicate entry" in str(error.__cause__) or
                    "UNIQUE constraint failed" in str(error.__cause__)):
                        return render(
                            request,
                            ("cbar_db/forms/private/"
                                "rider_eval_checklist_form.html"),
                            {
                                'form': form,
                                'error_text': (
                                    ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                    .format(form="Rider Eval Checklist Form")
                                ),
                            }
                        )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/private/rider_eval_checklist_form.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # Redirect to the 'you saved this form page':
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

        else:
            # The form is not valid
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/private/rider_eval_checklist_form.html",
                {
                    'form': form,
                    'participant': participant,
                    'error_text': ERROR_TEXT_FORM_INVALID
                }
            )

    else:
        # If request type is GET (or any other method) create a blank form.
        form=forms.RiderEvalChecklistForm()

        try:
            participant=models.Participant.objects.get(
                participant_id=participant_id
            )
        except ObjectDoesNotExist:
            # The participant doesn't exist.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/private/rider_eval_checklist_form.html",
                {
                    'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                }
            )

        return render(
            request,
            'cbar_db/forms/private/rider_eval_checklist_form.html',
            {
                'form': form,
                "participant": participant
            }
        )

@login_required
def index_admin(request):
    """ Logged in user index view. """

    return render(
        request,
        "cbar_db/admin/admin.html",
    )

@login_required
def report_select_participant(request):
    """ Logged in user select participant record view. """
    participants=models.Participant.objects.all()

    return render(
        request,
        'cbar_db/admin/reports/participant_select.html',
        {'participants':participants}
    )

@login_required
def index_private_forms(request):
    """ Private forms index view. """
    participants=models.Participant.objects.all()

    return render(
        request,
        "cbar_db/forms/private/private.html",
        {"participants": participants}
    )

@login_required
def participant_record(request, participant_id):
    """ Participant record view. """

    try:
        participant=models.Participant.objects.get(
            participant_id=participant_id
        )
    except ObjectDoesNotExist:
        # The participant doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/participant.html",
            {
                'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
            }
        )

    # Find our Participant's MediaRelease instances
    media_releases=models.MediaRelease.objects.filter(
        participant_id=participant
    )

    # Find our Participant's MedicalInfo instances
    medical_releases=models.MedicalInfo.objects.filter(
        participant_id=participant
    )

    # Find our Participant's AuthorizeEmergencyMedicalTreatment instances
    emergency_authorizations=(models.AuthorizeEmergencyMedicalTreatment
        .objects.filter(
            participant_id=participant
        )
    )

    # Find our Participant's LiabilityRelease instances
    liability_releases=(models.LiabilityRelease.objects.filter(
            participant_id=participant
        )
    )

    # Find our Participant's BackgroundCheck instances
    background_checks=(models.BackgroundCheck.objects.filter(
            participant_id=participant
        )
    )

    # Find our Participant's SeizureEval instances
    seizure_evals=(models.SeizureEval.objects.filter(
            participant_id=participant
        )
    )

    return render(
        request,
        "cbar_db/admin/reports/participant.html",
        {
            "participant": participant,
            "media_releases": media_releases,
            "medical_releases": medical_releases,
            "emergency_authorizations": emergency_authorizations,
            "liability_releases": liability_releases,
            "background_checks": background_checks,
            "seizure_evals": seizure_evals
        }
    )

@login_required
def report_media_release(request, participant_id, year, month, day):
    """ Displays a the data entered in a previous Media Release form. """

    # Find the participant's Participant record:
    try:
        participant=models.Participant.objects.get(
            participant_id=participant_id
        )
    except ObjectDoesNotExist:
        # The participant doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_media.html",
            {
                'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
            }
        )

    # Parse the Media Release's date from the URL attributes
    try:
        loggeyMcLogging.error("year, month, day=" + year + "," + month + "," + day)
        date=time.strptime(year + "/" + month + "/" + day, "%Y/%m/%d")
        loggeyMcLogging.error("Date=" + str(date))
    except:
        loggeyMcLogging.error("Couldn't parse the date")
        # The requested date can't be parsed
        return render(
            request,
            "cbar_db/admin/reports/report_media.html",
            {
                'error_text': ERROR_TEXT_INVALID_DATE,
            }
        )

    # Find the MediaRelease record:
    try:
        media_release=models.MediaRelease.objects.get(
            participant_id=participant,
            date=time.strftime("%Y-%m-%d", date)
        )
    except ObjectDoesNotExist:
        # The MediaRelease doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_media.html",
            {
                'error_text': ERROR_TEXT_MEDIA_RELEASE_NOT_AVAILABLE,
            }
        )

    return render(
        request,
        "cbar_db/admin/reports/report_media.html",
        {
            "media_release": media_release,
            "participant": participant
        }
    )

@login_required
def report_emerg_auth(request, participant_id, year, month, day):
    """ Displays the data entered in a previous Emergency Medical
     Authorization form. """

    # Find the participant's Participant record:
    try:
        participant=models.Participant.objects.get(
            participant_id=participant_id
        )
    except ObjectDoesNotExist:
        # The participant doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_emerg_auth.html",
            {
                'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
            }
        )

    # Parse the Emergency Medical Treatment Authorization's date from the
    # URL attributes:
    try:
        loggeyMcLogging.error("year, month, day=" + year + "," + month + "," + day)
        date=time.strptime(year + "/" + month + "/" + day, "%Y/%m/%d")
        loggeyMcLogging.error("Date=" + str(date))
    except:
        loggeyMcLogging.error("Couldn't parse the date")
        # The requested date can't be parsed
        return render(
            request,
            "cbar_db/admin/reports/report_emerg_auth.html",
            {
                'error_text': ERROR_TEXT_INVALID_DATE,
            }
        )

    # Find the AuthorizeEmergencyMedicalTreatment record:
    try:
        emerg_auth=models.AuthorizeEmergencyMedicalTreatment.objects.get(
            participant_id=participant,
            date=time.strftime("%Y-%m-%d", date)
        )
    except ObjectDoesNotExist:
        # The AuthorizeEmergencyMedicalTreatment record doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_emerg_auth.html",
            {
                'error_text': ERROR_TEXT_EMERG_AUTH_NOT_AVAILABLE,
            }
        )

    # Find the MedicalInfo record:
    try:
        medical_info=models.MedicalInfo.objects.get(
            participant_id=participant,
            date=time.strftime("%Y-%m-%d", date)
        )
    except ObjectDoesNotExist:
        # The MedicalInfo record doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_emerg_auth.html",
            {
                'error_text': ERROR_TEXT_MEDICAL_INFO_NOT_FOUND,
            }
        )

    return render(
        request,
        "cbar_db/admin/reports/report_emerg_auth.html",
        {
            "emerg_auth": emerg_auth,
            "medical_info": medical_info,
            "participant": participant
        }
    )

@login_required
def report_med_release(request, participant_id, year, month, day):
    """ Displays the data entered in a previous Medical Release/Info form. """

    # Find the participant's Participant record:
    try:
        participant=models.Participant.objects.get(
            participant_id=participant_id
        )
    except ObjectDoesNotExist:
        # The participant doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_med_release.html",
            {
                'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
            }
        )

    # Parse the Medical Release's date from the URL attributes:
    try:
        loggeyMcLogging.error("year, month, day=" + year + "," + month + "," + day)
        date=time.strptime(year + "/" + month + "/" + day, "%Y/%m/%d")
        loggeyMcLogging.error("Date=" + str(date))
    except:
        # The requested date can't be parsed
        loggeyMcLogging.error("Couldn't parse the date")

        return render(
            request,
            "cbar_db/admin/reports/report_med_release.html",
            {
                'error_text': ERROR_TEXT_INVALID_DATE,
            }
        )

    # Find the MedicalInfo record:
    try:
        medical_info=models.MedicalInfo.objects.get(
            participant_id=participant,
            date=time.strftime("%Y-%m-%d", date)
        )
    except ObjectDoesNotExist:
        # The MedicalInfo doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_med_release.html",
            {
                'error_text': ERROR_TEXT_MEDICAL_INFO_NOT_FOUND,
            }
        )

    # Find any Medication record(s):
    medications=models.Medication.objects.filter(
        participant_id=participant,
        date=time.strftime("%Y-%m-%d", date)
    )

    return render(
        request,
        "cbar_db/admin/reports/report_med_release.html",
        {
            "participant": participant,
            "medical_info": medical_info,
            "medications": medications
        }
    )

@login_required
def report_liability(request, participant_id, year, month, day):
    """ Displays the data entered in a previous Liability Release form. """

    # Find the participant's Participant record:
    try:
        participant=models.Participant.objects.get(
            participant_id=participant_id
        )
    except ObjectDoesNotExist:
        # The participant doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_liability.html",
            {
                'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
            }
        )

    # Parse the Liability Release's date from the URL attributes
    try:
        loggeyMcLogging.error("year, month, day=" + year + "," + month + "," + day)
        date=time.strptime(year + "/" + month + "/" + day, "%Y/%m/%d")
        loggeyMcLogging.error("Date=" + str(date))
    except:
        loggeyMcLogging.error("Couldn't parse the date")
        # The requested date can't be parsed
        return render(
            request,
            "cbar_db/admin/reports/report_liability.html",
            {
                'error_text': ERROR_TEXT_INVALID_DATE,
            }
        )

    # Find the LiabilityRelease record:
    try:
        liability_release=models.LiabilityRelease.objects.get(
            participant_id=participant,
            date=time.strftime("%Y-%m-%d", date)
        )
    except ObjectDoesNotExist:
        # The LiabilityRelease doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_liability.html",
            {
                'error_text': ERROR_TEXT_LIABILITY_RELEASE_NOT_AVAILABLE
            }
        )

    return render(
        request,
        "cbar_db/admin/reports/report_liability.html",
        {
            "liability_release": liability_release,
            "participant": participant
        }
    )

@login_required
def report_background(request, participant_id, year, month, day):
    """ Displays the data entered in a previous Background Check Authorization
     form. """

    # Find the participant's Participant record:
    try:
        participant=models.Participant.objects.get(
            participant_id=participant_id
        )
    except ObjectDoesNotExist:
        # The participant doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_background.html",
            {
                'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
            }
        )

    # Parse the Background Check Authorization's date from the URL attributes
    try:
        loggeyMcLogging.error("year, month, day=" + year + "," + month + "," + day)
        date=time.strptime(year + "/" + month + "/" + day, "%Y/%m/%d")
        loggeyMcLogging.error("Date=" + str(date))
    except:
        loggeyMcLogging.error("Couldn't parse the date")
        # The requested date can't be parsed
        return render(
            request,
            "cbar_db/admin/reports/report_background.html",
            {
                'error_text': ERROR_TEXT_INVALID_DATE,
            }
        )

    # Find the BackgroundCheck record:
    try:
        background_check=models.BackgroundCheck.objects.get(
            participant_id=participant,
            date=time.strftime("%Y-%m-%d", date)
        )
    except ObjectDoesNotExist:
        # The BackgroundCheck doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_background.html",
            {
                'error_text': ERROR_TEXT_BACKGROUND_CHECK_NOT_AVAILABLE
            }
        )

    return render(
        request,
        "cbar_db/admin/reports/report_background.html",
        {
            "background_check": background_check,
            "participant": participant
        }
    )

@login_required
def report_seizure(request, participant_id, year, month, day):
    """ Displays the data entered in a previous Seizure Evaluation form. """

    # Find the participant's Participant record:
    try:
        participant=models.Participant.objects.get(
            participant_id=participant_id
        )
    except ObjectDoesNotExist:
        # The participant doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_seizure.html",
            {
                'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
            }
        )

    # Parse the SeizureEval's date from the URL attributes
    try:
        loggeyMcLogging.error("year, month, day=" + year + "," + month + "," + day)
        date=time.strptime(year + "/" + month + "/" + day, "%Y/%m/%d")
        loggeyMcLogging.error("Date=" + str(date))
    except:
        loggeyMcLogging.error("Couldn't parse the date")
        # The requested date can't be parsed
        return render(
            request,
            "cbar_db/admin/reports/report_seizure.html",
            {
                'error_text': ERROR_TEXT_INVALID_DATE,
            }
        )

    # Find the SeizureEval record:
    try:
        seizure_eval=models.SeizureEval.objects.get(
            participant_id=participant,
            date=time.strftime("%Y-%m-%d", date)
        )
    except ObjectDoesNotExist:
        # The SeizureEval doesn't exist.
        # Set the error message and redisplay the form:
        return render(
            request,
            "cbar_db/admin/reports/report_seizure.html",
            {
                'error_text': ERROR_TEXT_SEIZURE_EVAL_NOT_AVAILABLE
            }
        )

    medications=models.Medication.objects.filter(
        participant_id=participant,
        date=time.strftime("%Y-%m-%d", date)
    )

    return render(
        request,
        "cbar_db/admin/reports/report_seizure.html",
        {
            "seizure_eval": seizure_eval,
            "medications": medications,
            "participant": participant
        }
    )

@login_required
def observation_evaluation(request, participant_id):
    if request.method == 'POST':
        form=forms.ObservationEvaluation(request.POST)

        try:
            participant=models.Participant.objects.get(
                participant_id=participant_id
            )
        except ObjectDoesNotExist:
            return render(
                request,
                "cbar_db/forms/private/observation_evaluation.html",
                {
                    'error_text':(ERROR_TEXT_PARTICIPANT_NOT_FOUND),
                }
            )

        if form.is_valid():
            try:
                form_data_observation=models.ObservationEvaluation(
                    participant_id=participant,
                    date=form.cleaned_data['date'],
                )
                form_data_observation.save()

            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/private/observation_evaluation.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="observation evaluation")
                            ),
                            "participant": participant
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/private/observation_evaluation.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )
            try:
                form_data_attitude=models.EvalAttitude(
                    participant_id=participant,
                    date=form.cleaned_data['date'],

                    walking_through_barn_willing=form.cleaned_data['walking_through_barn_willing'],
                    walking_through_barn_motivated=form.cleaned_data['walking_through_barn_motivated'],
                    walking_through_barn_appearance=form.cleaned_data['walking_through_barn_appearance'],

                    looking_at_horses_willing=form.cleaned_data['looking_at_horses_willing'],
                    looking_at_horses_motivated=form.cleaned_data['looking_at_horses_motivated'],
                    looking_at_horses_appearance=form.cleaned_data['looking_at_horses_appearance'],

                    petting_horses_willing=form.cleaned_data['petting_horses_willing'],
                    petting_horses_motivated=form.cleaned_data['petting_horses_motivated'],
                    petting_horses_appearance=form.cleaned_data['petting_horses_appearance'],

                    up_down_ramp_willing=form.cleaned_data['up_down_ramp_willing'],
                    up_down_ramp_motivated=form.cleaned_data['up_down_ramp_motivated'],
                    up_down_ramp_appearance=form.cleaned_data['up_down_ramp_appearance'],

                    mounting_before_willing=form.cleaned_data['mounting_before_willing'],
                    mounting_before_motivated=form.cleaned_data['mounting_before_motivated'],
                    mounting_before_appearance=form.cleaned_data['mounting_before_appearance'],

                    mounting_after_willing=form.cleaned_data['mounting_after_willing'],
                    mounting_after_motivated=form.cleaned_data['mounting_after_motivated'],
                    mounting_after_appearance=form.cleaned_data['mounting_after_appearance'],

                    riding_before_willing=form.cleaned_data['riding_before_willing'],
                    riding_before_motivated=form.cleaned_data['riding_before_motivated'],
                    riding_before_appearance=form.cleaned_data['riding_before_appearance'],

                    riding_during_willing=form.cleaned_data['riding_during_willing'],
                    riding_during_motivated=form.cleaned_data['riding_during_motivated'],
                    riding_during_appearance=form.cleaned_data['riding_during_appearance'],

                    riding_after_willing=form.cleaned_data['riding_after_willing'],
                    riding_after_motivated=form.cleaned_data['riding_after_motivated'],
                    riding_after_appearance=form.cleaned_data['riding_after_appearance'],

                    understands_directions_willing=form.cleaned_data['understands_directions_willing'],
                    understands_directions_motivated=form.cleaned_data['understands_directions_motivated'],
                    understands_directions_appearance=form.cleaned_data['understands_directions_appearance'],

                    participates_exercises_willing=form.cleaned_data['participates_exercises_willing'],
                    participates_exercises_motivated=form.cleaned_data['participates_exercises_motivated'],
                    participates_exercises_appearance=form.cleaned_data['participates_exercises_appearance'],

                    participates_games_willing=form.cleaned_data['participates_games_willing'],
                    participates_games_motivated=form.cleaned_data['participates_games_motivated'],
                    participates_games_appearance=form.cleaned_data['participates_games_appearance'],

                    general_attitude_willing=form.cleaned_data['general_attitude_willing'],
                    general_attitude_motivated=form.cleaned_data['general_attitude_motivated'],
                    general_attitude_appearance=form.cleaned_data['general_attitude_appearance'],
                )
                form_data_attitude.save()

            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/private/observation_evaluation.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="observation evaluation")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/private/observation_evaluation.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

        else:

            return render(
                request,
                "cbar_db/forms/private/observation_evaluation.html",
                {
                    'form':form,
                    'error_text':"Error validating form.",
                    "participant": participant
                }
            )
    else:
        try:
            participant=models.Participant.objects.get(
                participant_id=participant_id
            )
        except ObjectDoesNotExist:
            return render(
                request,
                "cbar_db/forms/private/observation_evaluation.html",
                {
                    'error_text':(ERROR_TEXT_PARTICIPANT_NOT_FOUND),
                }
            )

        form=forms.ObservationEvaluation()

        return render(
            request,
            'cbar_db/forms/private/observation_evaluation.html',
            {
                'form': form,
                'participant': participant
            }
        )

@login_required
def private_form_session_plan(request, participant_id):
    """Data for session plan form."""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        # Create a form instance and populate it with data from the request:
        form=forms.SessionPlanForm(request.POST)

        # Check whether the form data entered is valid:
        if form.is_valid():
            loggeyMcLogging.error("The form is valid")
            # Find the participant's record based on their (name, birth_date):
            try:
                participant=models.Participant.objects.get(
                    participant_id=participant_id
                )
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/private/session_plan.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                    }
                )

            session_plan=models.Session(
                date=form.cleaned_data['date'],
                tack=form.cleaned_data['tack']
            )
            session_plan.save()

            session_ind=models.SessionPlanInd(
                participant_id=participant,
                date=form.cleaned_data["date"],
                horse_leader=form.cleaned_data['horse_leader']
            )
            session_ind.save()

            session_goals=models.SessionGoals(
                participant_id=participant,
                session_id=session_plan,
                goal_type=form.cleaned_data['goal_type'],
                goal_description=form.cleaned_data['goal_description'],
                motivation=form.cleaned_data['motivation']
            )
            session_goals.save()

            horse_info=models.Horse(
                name=form.cleaned_data['horse_name'],
            )
            horse_info.save()

            try:
                adaptations_needed=models.AdaptationsNeeded(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    ambulatory_status=form.cleaned_data['ambulatory_status'],
                    ambulatory_status_other=(
                        form.cleaned_data['ambulatory_status_other']),
                    mount_assistance_required=(
                        form.cleaned_data['mount_assistance_required']),
                    mount_device_needed=(
                        form.cleaned_data['mount_device_needed']),
                    mount_type=(
                        form.cleaned_data['mount_type']),
                    dismount_assistance_required=(
                        form.cleaned_data['dismount_assistance_required']),
                    dismount_type=form.cleaned_data['dismount_type'],
                    num_sidewalkers_walk_spotter=(
                        form.cleaned_data["num_sidewalkers_walk_spotter"]),
                    num_sidewalkers_walk_heel_hold=(
                        form.cleaned_data["num_sidewalkers_walk_heel_hold"]),
                    num_sidewalkers_walk_over_thigh=(
                        form.cleaned_data["num_sidewalkers_walk_over_thigh"]),
                    num_sidewalkers_walk_other=(
                        form.cleaned_data["num_sidewalkers_walk_other"]),
                    num_sidewalkers_trot_spotter=(
                        form.cleaned_data["num_sidewalkers_trot_spotter"]),
                    num_sidewalkers_trot_heel_hold=(
                        form.cleaned_data["num_sidewalkers_trot_heel_hold"]),
                    num_sidewalkers_trot_over_thigh=(
                        form.cleaned_data["num_sidewalkers_trot_over_thigh"]),
                    num_sidewalkers_trot_other=(
                        form.cleaned_data["num_sidewalkers_trot_other"])
                )
                adaptations_needed.save()
            # Catch duplicate primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/private/session_plan.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="session plan")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/private/session_plan.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # redirect to a "you saved a form" page:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

        else:
            # The form is not valid
            loggeyMcLogging.error("The form is NOT valid")

            try:
                participant=models.Participant.objects.get(
                    participant_id=participant_id
                )
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/private/session_plan.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                    }
                )

            return render(
                request,
                "cbar_db/forms/private/session_plan.html",
                {
                    'form': form,
                    'participant': participant,
                    'error_text': ERROR_TEXT_FORM_INVALID,
                }
            )
    else:
        # If request type is GET (or any other method) create a blank form and
        # display it:
        form=forms.SessionPlanForm()

        try:
            participant=models.Participant.objects.get(
                participant_id=participant_id
            )
        except ObjectDoesNotExist:
            # The participant doesn't exist.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/private/session_plan.html",
                {
                    'form': form,
                    'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                }
            )

        diagnosis_types=models.Diagnosis.objects.filter(
            participant_id=participant,
        )

        return render(
            request,
            'cbar_db/forms/private/session_plan.html',
            {
                'form': form,
                'participant': participant,
                'diagnosis_types': diagnosis_types
            }
        )

@login_required
def private_form_phone_log(request, participant_id):
    """Data for phone log form."""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        # Create a form instance and populate it with data from the request:
        form=forms.PhoneLogForm(request.POST)

        # Check whether the form data entered is valid:
        if form.is_valid():
            loggeyMcLogging.error("The form is valid")
            # Find the participant's record based on their (name, birth_date):
            try:
                participant=models.Participant.objects.get(
                    participant_id=participant_id
                )
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/private/phone_log.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                    }
                )
            try:
                phone_log=models.PhoneLog(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    time=form.cleaned_data["time"],
                    details=form.cleaned_data["details"]
                )
                phone_log.save()
            # Catch duplicate primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/private/phone_log.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="phone log")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/private/phone_log.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # redirect to a "you saved a form" page:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

        else:
            # The form is not valid
            loggeyMcLogging.error("The form is NOT valid")

            try:
                participant=models.Participant.objects.get(
                    participant_id=participant_id
                )
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/private/phone_log.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                    }
                )

            return render(
                request,
                "cbar_db/forms/private/phone_log.html",
                {
                    'form': form,
                    'participant': participant,
                    'error_text': ERROR_TEXT_FORM_INVALID,
                }
            )
    else:
        # If request type is GET (or any other method) create a blank form and
        # display it:
        form=forms.PhoneLogForm()

        try:
            participant=models.Participant.objects.get(
                participant_id=participant_id
            )
        except ObjectDoesNotExist:
            # The participant doesn't exist.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/private/phone_log.html",
                {
                    'form': form,
                    'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                }
            )

        return render(
            request,
            "cbar_db/forms/private/phone_log.html",
            {
                'form': form,
                'participant': participant
            }
        )

@login_required
def private_form_incidents(request, participant_id):
    """Data for incidents form."""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        loggeyMcLogging.error("Request is of type POST")
        # Create a form instance and populate it with data from the request:
        form=forms.IncidentsForm(request.POST)

        # Check whether the form data entered is valid:
        if form.is_valid():
            loggeyMcLogging.error("The form is valid")
            # Find the participant's record based on their (name, birth_date):
            try:
                participant=models.Participant.objects.get(
                    participant_id=participant_id
                )
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/private/incidents.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                    }
                )

            try:
                incidents=models.Incidents(
                    participant_id=participant,
                    date=form.cleaned_data["date"],
                    time=form.cleaned_data["time"],
                    details=form.cleaned_data["details"]
                )
                incidents.save()
            # Catch duplicate primary keys:
            except IntegrityError as error:
                # Set the error message and redisplay the form:
                if "Duplicate entry" in str(error.__cause__) or "UNIQUE constraint failed" in str(error.__cause__):
                    return render(
                        request,
                        "cbar_db/forms/private/incidents.html",
                        {
                            'form': form,
                            'error_text': (
                                ERROR_TEXT_DUPLICATE_PARTICIPANT_DATE_PK
                                .format(form="incidents")
                            ),
                        }
                    )
                else: # pragma: no cover
                    # Excluded from coverage results because no way to test
                    # without intentionally breaking validation code
                    loggeyMcLogging.error(
                        "Caught generic database exception:\n" + str(error)
                    )
                    return render(
                        request,
                        "cbar_db/forms/private/incidents.html",
                        {
                            'form': form,
                            'error_text': ERROR_TEXT_DB_INTEGRITY,
                        }
                    )

            # redirect to a "you saved a form" page:
            return HttpResponseRedirect(reverse("form-saved")+"?a=a")

        else:
            # The form is not valid
            loggeyMcLogging.error("The form is NOT valid")

            try:
                participant=models.Participant.objects.get(
                    participant_id=participant_id
                )
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/private/incidents.html",
                    {
                        'form': form,
                        'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                    }
                )

            return render(
                request,
                "cbar_db/forms/private/incidents.html",
                {
                    'form': form,
                    'participant': participant,
                    'error_text': ERROR_TEXT_FORM_INVALID,
                }
            )
    else:
        # If request type is GET (or any other method) create a blank form and
        # display it:
        form=forms.IncidentsForm()

        try:
            participant=models.Participant.objects.get(
                participant_id=participant_id
            )
        except ObjectDoesNotExist:
            # The participant doesn't exist.
            # Set the error message and redisplay the form:
            return render(
                request,
                "cbar_db/forms/private/incidents.html",
                {
                    'form': form,
                    'error_text': ERROR_TEXT_PARTICIPANT_NOT_FOUND,
                }
            )
        return render(
            request,
            "cbar_db/forms/private/incidents.html",
            {
                'form': form,
                'participant': participant
            }
        )
