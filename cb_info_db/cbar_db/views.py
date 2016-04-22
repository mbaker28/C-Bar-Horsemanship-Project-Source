from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django import forms as django_forms
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
                # Create a new ApplicationForm for the participant and save it:
                form_data_application=models.Participant(
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
                    address_state=form.cleaned_data['address_state'],
                    address_zip=form.cleaned_data['address_zip'],
                    phone_home=form.cleaned_data['phone_home'],
                    phone_cell=form.cleaned_data['phone_cell'],
                    phone_work=form.cleaned_data['phone_work'],
                    email=form.cleaned_data['email'],

                    # TODO: These two fields don't exist in the Participant
                    #       class. Do we even need them?
                    #           signature=form.cleaned_data['signature'],
                    #           date=form.cleaned_data['date']
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
            form_data_liability=models.LiabilityRelease(
                participant_id=participant,
                signature=form.cleaned_data['signature'],
                date=form.cleaned_data['date']
            )
            form_data_liability.save()

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

            public_form_background=models.BackgroundCheck(
                participant_id=participant,
                date=form.cleaned_data['date'],
                signature=form.cleaned_data['signature'],
                driver_license_num=form.cleaned_data['driver_license_num']
            )
            public_form_background.save()

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
            )
            seizure_data.save()

            if form.cleaned_data["seizure_name_one"] != "":
                seizure_type_one=models.SeizureType(
                    seizure_eval=seizure_data,
                    name=form.cleaned_data['seizure_name_one']
                )
                seizure_type_one.save()

            if form.cleaned_data["seizure_name_two"] != "":
                seizure_type_two=models.SeizureType(
                    seizure_eval=seizure_data,
                    name=form.cleaned_data['seizure_name_two']
                )
                seizure_type_two.save()

            if form.cleaned_data["seizure_name_three"] != "":
                seizure_type_three=models.SeizureType(
                    seizure_eval=seizure_data,
                    name=form.cleaned_data['seizure_name_three']
                )
                seizure_type_three.save()

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

@login_required
def index_private_admin(request):
    """ Logged in user index view. """
    participants=models.Participant.objects.all()

    return render(
        request,
        'cbar_db/admin/admin.html',
        {'participants':participants}
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
            "cbar_db/admin/participant.html",
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
        "cbar_db/admin/participant.html",
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

    seizure_types=models.SeizureType.objects.filter(
        seizure_eval=seizure_eval
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
            "seizure_types": seizure_types,
            "medications": medications,
            "participant": participant
        }
    )

@login_required
def private_form_intake_assessment_select_participants(request):
    """ First page of the intake assessment view. Handles selection of
     participant(s) to evaluate during the assessment. """

    class SelectedParticipantsForm(django_forms.Form):
        participants_selected=django_forms.ModelMultipleChoiceField(
            queryset=models.Participant.objects.all(),
            widget=django_forms.CheckboxSelectMultiple,
        )

    if request.method == "POST":
        # The user submitted their selections -> process things.
        loggeyMcLogging.error("Request type is POST.")

        form=SelectedParticipantsForm(request.POST)

        # Log things for debugging / testing purposes:
        loggeyMcLogging.error("request.POST == " + str(request.POST))
        loggeyMcLogging.error(
            "request.POST.getlist(\"participants_selected\") == " +
            str(request.POST.getlist("participants_selected"))
        )

        # Retreive the participant id numbers passed from the POST date:
        selected_participant_id_numbers=(
            request.POST.getlist("participants_selected")
        )

        # Retreive a Participant record for each ID number:
        selected_participants=[]
        loggeyMcLogging.error("Retrieving selected participants...")
        for participant in selected_participant_id_numbers:
            try:
                loggeyMcLogging.error(
                    "Retrieving participant with ID " + str(participant) + "..."
                )

                selected_participants.append(
                    models.Participant.objects.get(
                        participant_id=participant
                    )
                )

                loggeyMcLogging.error(
                    "Retrieved participant with ID " + str(participant) + "."
                )
            except:
                loggeyMcLogging.error(
                    "ERROR: Couldn't retrieve participant with ID "
                     + str(participant) + "!"
                )

        loggeyMcLogging.error(str(selected_participants))

        # Load the form template and pass the selected participants to it:
        return render(
            request,
            'cbar_db/forms/private/intake_assessment_form.html',
            {
                "selected_participants":selected_participants,
            }
        )

    else:
        # Normal request type -> display things.
        loggeyMcLogging.error("Request type is " + request.method + ".")

        form=SelectedParticipantsForm()
        participants=models.Participant.objects.all()

        return render(
            request,
            'cbar_db/forms/private/intake_assessment_participants.html',
            {
                "participants":participants,
                "form": form
            }
        )

@login_required
def private_form_intake_assessment(request):
    """ Intake form view. Handles both single and multiple participant versions
     of the form. """
