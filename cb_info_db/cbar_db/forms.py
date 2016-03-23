from django import forms
from cbar_db import models

class MedicalReleaseForm(forms.Form):
    primary_physician_name=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("primary_physician_name").max_length
    )

    primary_physician_phone=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("primary_physician_phone").max_length
    )

    last_seen_by_physician_date=forms.DateField()

    last_seen_by_physician_reason=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("last_seen_by_physician_reason").max_length
    )

    
