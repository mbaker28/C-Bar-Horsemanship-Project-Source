from django import forms
from cbar_db import models

class MediaReleaseForm(forms.Form):
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )

    consent=forms.ChoiceField(
        choices=models.MediaRelease._meta.get_field("consent").choices
    )

    signature=forms.CharField(
        max_length=models.MediaRelease._meta.get_field("signature").max_length
    )

    date=forms.DateField()
