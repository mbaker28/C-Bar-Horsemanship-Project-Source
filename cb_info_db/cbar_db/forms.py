from django import forms
from cbar_db import models

class MediaReleaseForm(forms.Form):
    name = forms.CharField(
        label='Your name',
        max_length=20 # models.Participant.name.max_length
    )
