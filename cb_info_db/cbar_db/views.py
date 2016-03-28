# from django.http import HttpResponse
from django.shortcuts import render
from cbar_db import forms

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
    """ Medical Release form view. Handles viewing and saving the form.

    Viewing form (GET): Display the form
    Saving form (POST):
        -Do something
    """

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # Do stuff
        print("Doing something...")
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
    """ Emegency Medical Treatment Authorization form view. """
    return render(request, 'cbar_db/forms/public/emergency_authorization.html')


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
