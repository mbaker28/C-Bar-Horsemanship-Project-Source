from django import forms
from cbar_db import models

class LiabilityReleaseForm(forms.Form):
    name = forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )
    
    birth_date = forms.DateField()

    signature=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("signature").max_length
    )
    date = forms.DateField()
