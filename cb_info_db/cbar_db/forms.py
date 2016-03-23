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
        max_length=(models.MedicalInfo._meta
            .get_field("last_seen_by_physician_reason").max_length
        )
    )

    allergies_conditions_that_exclude=forms.BooleanField()

    allergies_conditions_that_exclude_description=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("allergies_conditions_that_exclude_description").max_length
        #null=true... what needs to be done for this???
    )

    heat_exhaustion_stroke=forms.BooleanField()

    tetanus_shot_last_ten_years=forms.BooleanField()

    seizures_last_six_monthes=forms.BooleanField()

    #currently taking medications code goes here
    medication_one_name=forms.CharField(
        max_length=models.Medication._meta.get_field("medication_name").max_length
    )
    medication_one_duration=forms.CharField(
        max_length=models.Medication._meta.get_field("duration_taken").max_length
    )
    medication_one_frequency=forms.CharField(
        max_length=models.Medication._meta.get_field("frequency").max_length
    )

    medication_two_name=forms.CharField(
        max_length=models.Medication._meta.get_field("medication_name").max_length
    )
    medication_two_duration=forms.CharField(
        max_length=models.Medication._meta.get_field("duration_taken").max_length
    )
    medication_two_frequency=forms.CharField(
        max_length=models.Medication._meta.get_field("frequency").max_length
    )

    doctor_concered_re_horse_activites=forms.BooleanField() # If yes -> PhysRelease required

    physical_or_mental_issues_affecting_riding=forms.BooleanField()

    physical_or_mental_issues_affecting_riding_description=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("physical_or_mental_issues_affecting_riding_description").max_length
        #null=true... what needs to be done for this???
    )

    restriction_for_horse_activity_last_five_years=forms.BooleanField()

    restriction_for_horse_activity_last_five_years_description=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("restriction_for_horse_activity_last_five_years_description").max_length
        #null=true... what needs to be done for this???
    )

    present_restrictions_for_horse_activity=forms.BooleanField() # If yes -> PhysRelease required

    limiting_surgeries_last_six_monthes=forms.BooleanField()

    signature=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("signature").max_length
    )

    date=forms.DateField()
