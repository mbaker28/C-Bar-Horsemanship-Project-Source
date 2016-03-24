# from django.http import HttpResponse
from django.shortcuts import render

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
        # create a form instance and populate it with data from the request:
        form=form.EmergencyMedicalReleaseForm(request.POST)
        #chech whether it's valid:
        if form.is_valid():
            #create an instance of the EmergencyMedicalReleaseForm model to hold form data
            logger.error("Creating Emergency Medical Release Form instance...")
            try:
                form_data_emerg_auth=models.EmergencyMedicalReleaseForm(
                    participant_id=models.Participant.objects.get(
                        name=form.cleaned_data['name']
                    ),
                    # TODO: birth_date needs to be updated in relavenent participant instance
                )
                logger.error("Saving Emergency Medical Release Form instance...")
                new_data=form_data_media.save()
                logger.error("Successfully saved Emergency Medical Release Form")
            except objectDoesNotExsist:
                """Triggered if the PK found by name doesn't exist
                    AKA:The Participant record Doesn't exist.
                """
                logger.error(
                    "Couldn't find Participant FK to save Emergency Medical Release Form"
                    )
            #redirec to a new URL:
            return HttpResponseRedirect('/')

        #if a GET (or any other method) we'll create a black for,
        else:
            form=forms.EmergencyMedicalReleaseForm()

        return render(request, 'cbar_db/forms/public/media.html', {'form': form})


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
