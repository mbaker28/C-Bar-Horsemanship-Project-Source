from django import forms
from cbar_db import models

class MedicalReleaseForm(forms.Form):
    primary_physician_name=forms.CharField(
        max_length=(models.MedicalInfo._meta
            .get_field("primary_physician_name").max_length
        )
    )

    primary_physician_phone=forms.CharField(
        max_length=(models.MedicalInfo._meta
            .get_field("primary_physician_phone").max_length
        )
    )

    last_seen_by_physician_date=forms.DateField()

    last_seen_by_physician_reason=forms.CharField(
        max_length=(models.MedicalInfo._meta
            .get_field("last_seen_by_physician_reason").max_length
        )
    )

    allergies_conditions_that_exclude=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("allergies_conditions_that_exclude").choices
        )
    )

    allergies_conditions_that_exclude_description=forms.CharField(
        max_length=(models.MedicalInfo
            ._meta.get_field("allergies_conditions_that_exclude_description")
            .max_length
        ),
        required=False
    )

    heat_exhaustion_stroke=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("heat_exhaustion_stroke").choices
        )
    )

    tetanus_shot_last_ten_years=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("tetanus_shot_last_ten_years").choices
        )
    )

    seizures_last_six_monthes=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("seizures_last_six_monthes").choices
        )
    )

    #currently taking medications code goes here
    medication_one_name=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("medication_name").max_length
        )
    )
    medication_one_duration=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("duration_taken").max_length
        )
    )
    medication_one_frequency=forms.CharField(
        max_length=models.Medication._meta.get_field("frequency").max_length
    )

    medication_two_name=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("medication_name").max_length
        )
    )
    medication_two_duration=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("duration_taken").max_length
        )
    )
    medication_two_frequency=forms.CharField(
        max_length=models.Medication._meta.get_field("frequency").max_length
    )

    # If yes -> Physician Release required:
    doctor_concered_re_horse_activites=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("doctor_concered_re_horse_activites").choices
        )
    )

    physical_or_mental_issues_affecting_riding=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("physical_or_mental_issues_affecting_riding").choices
        )
    )

    physical_or_mental_issues_affecting_riding_description=forms.CharField(
        max_length=(models.MedicalInfo._meta
            .get_field("physical_or_mental_issues_affecting_riding_description")
            .max_length
        ),
        required=False
    )

    restriction_for_horse_activity_last_five_years=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("restriction_for_horse_activity_last_five_years").choices
        )
    )

    restriction_for_horse_activity_last_five_years_description=forms.CharField(
        max_length=(models.MedicalInfo._meta
            .get_field(
                "restriction_for_horse_activity_last_five_years_description"
            ).max_length
        ),
        required=False
    )

    # If yes -> Physician's Release required
    present_restrictions_for_horse_activity=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("present_restrictions_for_horse_activity").choices
        )
    )

    limiting_surgeries_last_six_monthes=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("limiting_surgeries_last_six_monthes").choices
        )
    )

    signature=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("signature").max_length
    )

    date=forms.DateField()
