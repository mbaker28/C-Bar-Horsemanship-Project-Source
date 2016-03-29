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
    """ Medical Release form view.
    """
    return render(request, 'cbar_db/forms/public/medical_release.html')


def public_form_emerg_auth(request):
    """ Emegency Medical Treatment Authorization form view. """
    return render(request, 'cbar_db/forms/public/emergency_authorization.html')


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
                        'error_text': ("The requested participant isn't in the"
                        " database."),
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
                    'error_text': "Error validating form.",
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
    """ Media Release form view. """
    return render(request, 'cbar_db/forms/public/media.html')


def public_form_background(request):
    """ Background Check Authorization form view. """
    return render(request, 'cbar_db/forms/public/background.html')


def public_form_seizure(request):
    """ Seizure Evaluation form view. """
    return render(request, 'cbar_db/forms/public/seizure.html')
