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
