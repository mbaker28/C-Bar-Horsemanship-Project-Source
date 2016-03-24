# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import logging
from cbar_db import forms
from cbar_db import models

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
            Create new record in MedicalInfo
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
            try:
                participant_id=models.Participant.objects.get(
                    name=form.cleaned_data['name']
                ).first()
            except ObjectDoesNotExist:
                # The participant doesn't exist.
                # Set the error message and redisplay the form:
                return render(
                    request,
                    "cbar_db/forms/public/emergency_authorization.html",
                    {
                        'form': form,
                        'error_text': ("The requested participant isn't in the"
                        " database."),
                    }
                )

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
                    'error_text': "Error validating form.",
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
    return render(request, 'cbar_db/forms/public/background.html')


def public_form_seizure(request):
    """ Seizure Evaluation form view. """
    return render(request, 'cbar_db/forms/public/seizure.html')
