# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
import logging
from cbar_db import forms
from cbar_db import models

logger = logging.getLogger()

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
    """ Emegency Medical Treatment Authorization form view. """
    return render(request, 'cbar_db/forms/public/emergency_authorization.html')


def public_form_liability(request):
    """ Liability Release form view. """
    return render(request, 'cbar_db/forms/public/liability.html')


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
            logger.error("Creating MediaRelease instance...")
            try:
                form_data_media=models.MediaRelease(
                    participant_id=models.Participant.objects.get(
                        name=form.cleaned_data['name']
                    ),
                    consent=form.cleaned_data['consent'],
                    signature=form.cleaned_data['signature'],
                    date=form.cleaned_data['date']
                )
                logger.error("Saving MediaRelease instance...")
                new_data=form_data_media.save()
                logger.error("Sucessfully saved Media Release form")
            except ObjectDoesNotExist:
                """ Triggered if the PK found by name doesn't exist
                    AKA: The participant record doesn't exist.
                 """
                logger.error(
                    "Couldn't find Participant FK to save media release form."
                )

        # redirect to a new URL:
        return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form=forms.MediaReleaseForm()

    return render(request, 'cbar_db/forms/public/media.html', {'form': form})


def public_form_background(request):
    """ Background Check Authorization form view. """
    return render(request, 'cbar_db/forms/public/background.html')


def public_form_seizure(request):
    """ Seizure Evaluation form view. """
    return render(request, 'cbar_db/forms/public/seizure.html')
