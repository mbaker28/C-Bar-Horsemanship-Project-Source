from django import forms
from cbar_db import models

class EmergencyMedicalReleaseForm(forms.Form):
    # Shit stored in Participant
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )
    birth_date=forms.DateField()

    # Shite stored in MedicalInfo
    primary_physician_name=forms.CharField(
        max_length=models.MedicalInfo._meta.field("primary_physician_name").max_length
    )
    primary_physician_phone=forms.CharField(
        max_length=models.MedicalInfo._meta.field("primary_physician_phone").max_length
    )

    # Shite stored in AuthorizeEmergencyMedicalTreatment
    pref_medical_facility=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .field("pref_medical_facility").max_length
        )
    )
    insurance_provider=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .field("insurance_provider").max_length
        )
    )
    insurance_policy_num=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .field("insurance_policy_num").max_length
        )
    )
    emerg_contact_name=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .field("emerg_contact_name").max_length
        )
    )
    emerg_contact_phone=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .field("emerg_contact_phone").max_length
        )
    )
    emerg_contact_relation=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .field("emerg_contact_relation").max_length
        )
    )
    consents_emerg_med_treatment=forms.CharField(
        choices=(models.AuthorizeEmergencyMedicalTreatment._meta
            .field("consents_emerg_med_treatment").choices
        )
    )
    date=forms.DateField()
    signature=forms.CharField(
        max_length=models.MedicalInfo._meta.field("signature").max_length
    )
