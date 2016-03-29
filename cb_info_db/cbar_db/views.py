from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import logging
from cbar_db import forms
from cbar_db import models

ERROR_TEXT_PARTICIPANT_NOT_FOUND=(
    "The requested participant isn't in the database."
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
    return render(request, 'cbar_db/forms/public/application.html')


def public_form_med_release(request):
    """ Medical Release form view. """
    return render(request, 'cbar_db/forms/public/medical_release.html')


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
    """ Liability Release form view. """
    return render(request, 'cbar_db/forms/public/liability.html')


def public_form_media(request):
    """ Media Release form view. """
    return render(request, 'cbar_db/forms/public/media.html')


def public_form_background(request):
    """ Background Check Authorization form view. """
    if request.method == 'POST':
        loggeyMclogging.error("Request is of type POST")
        form=forms.BackgroundCheckForm(request.POST)

    if form.is_valid():
        loggeyMclogging.error("The form is valid")
        try:
             participant=models.Participant.objects.get(
                    name=form.cleaned_data['name'],
                    birth_date=form.cleaned_data['birth_date']
                )
        except ObjectDoesNotExist:
            return render(
                request,
                "cbar_db/forms/public/public_form_background.html",
                {
                    'form': form,
                    'error_text': (ERROR_TEXT_PARTICIPANT_NOT_FOUND),
                }
            )
    return render(request, 'cbar_db/forms/public/background.html')


def public_form_seizure(request):
    """ Seizure Evaluation form view. """
    return render(request, 'cbar_db/forms/public/seizure.html')
