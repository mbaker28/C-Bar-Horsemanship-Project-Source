from django import forms
from cbar_db import models

class LiabilityReleaseForm(forms.Form):
    name = forms.CharField(
        label = 'Your name',
        max_length=models.Participant.name.max_length
    )

    signature=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("signature").max_length
    )

    date = forms.DateField()
