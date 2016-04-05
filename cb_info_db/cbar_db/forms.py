from django import forms
from cbar_db import models

class SeizureEvaluationForm(forms.Form):
    name=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("name").max_length
        )
    )

#addd a birth_date field

    date=forms.DateField()

    guardian_name=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("guardian_name").max_length
        )
    )

    phone_home=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("phone_home").max_length
        )
    )

    phone_cell=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("phone_cell").max_length
        )
    )

    phone_work=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("phone_work").max_length
        )
    )

    name=forms.CharField(                       #???????
        max_length=(models.SeizureType._meta    #???????
            .get_field("name").max_length           #???????
        )
    )

    date_of_last_seizure=forms.DateField()

    #needs a "frequency of seizures" field in models.py

    duration_of_last_seizure=forms.DurationField()

    typical_cause=forms.CharField(
        max_length=(models.SeizureEval._meta
            .get_field("typical_cause").max_length
        )
    )

    seizure_indicators=forms.CharField(
        max_length=(models.SeizureEval._meta
            .get_field("seizure_indicators").max_length
        )
    )

    after_effect=forms.CharField(
        max_length=(models.SeizureEval._meta
            .get_field("after_effect").max_length
        )
    )

    #what should I do for current medications field???????

    during_seizure_stare=forms.BooleanField()

    during_seizure_stare_length=forms.DurationField()

    during_seizure_walks=forms.BooleanField()

    during_seizure_aimless=forms.BooleanField()

    during_seizure_cry_etc=forms.BooleanField()

    during_seizure_bladder_bowel=forms.BooleanField()

    during_seizure_confused_etc=forms.BooleanField()

    #TODO: Rename during_seizure_other to during_seizure_other_description and
    #      and add a during_seizure_other BooleanField in models.py

    during_seizure_other=forms.CharField(
        max_length=(models.SeizureEval._meta
            .get_field("during_seizure_other").max_length
        )
    )

    knows_when_will_occur=forms.BooleanField()

    can_communicate_when_will_occur=forms.BooleanField()

    #not sure where "what are the signs?" field is on models.py

    actions_to_take=forms.ChoiceField(
        choices=(models.SeizureEval._meta
            .get_field("actions_to_take").choices
        )
    )

    # signature=forms.CharField(
    #     max_length=(models.SeizureEval._meta
    #         .get_field("signature").max_length
    #     )
    # )

    date=forms.DateField()

    #C-Bar staff signature needed in models.py

    date=forms.DateField()


class LiabilityReleaseForm(forms.Form):
    name = forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )

    birth_date = forms.DateField()

    signature=forms.CharField(
        max_length=models.LiabilityRelease._meta.get_field("signature").max_length
    )
    date = forms.DateField()


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

    currently_taking_any_medication=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("currently_taking_any_medication").choices
        )
    )
    medication_one_name=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("medication_name").max_length
        ),
        required=False
    )
    medication_one_duration=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("duration_taken").max_length
        ),
        required=False
    )
    medication_one_frequency=forms.CharField(
        max_length=models.Medication._meta.get_field("frequency").max_length,
        required=False
    )

    medication_two_name=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("medication_name").max_length
        ),
        required=False
    )
    medication_two_duration=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("duration_taken").max_length
        ),
        required=False
    )
    medication_two_frequency=forms.CharField(
        max_length=models.Medication._meta.get_field("frequency").max_length,
        required=False
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

    limiting_surgeries_last_six_monthes_description=forms.CharField(
        max_length=(models.MedicalInfo._meta
            .get_field("limiting_surgeries_last_six_monthes_description")
            .max_length
        ),
        required=False
    )

    birth_date=forms.DateField()

    signature=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("signature").max_length
    )

    date=forms.DateField()


class BackgroundCheckForm(forms.Form):
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )
    signature=forms.CharField(
        max_length=(models.BackgroundCheck._meta
            .get_field("signature").max_length
        )
    )
    date=forms.DateField()
    birth_date=forms.DateField()
    driver_license_num=forms.CharField(
        max_length=(models.BackgroundCheck._meta
            .get_field("driver_license_num").max_length
        )
    )


class MediaReleaseForm(forms.Form):
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )
    birth_date=forms.DateField()
    consent=forms.ChoiceField(
        choices=models.MediaRelease._meta.get_field("consent").choices
    )
    signature=forms.CharField(
        max_length=models.MediaRelease._meta.get_field("signature").max_length
    )
    date=forms.DateField()


class EmergencyMedicalReleaseForm(forms.Form):
    # Stored in Participant
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )
    birth_date=forms.DateField()

    # Stored in MedicalInfo
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

    # Stored in AuthorizeEmergencyMedicalTreatment
    pref_medical_facility=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("pref_medical_facility").max_length
        )
    )
    insurance_provider=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("insurance_provider").max_length
        )
    )
    insurance_policy_num=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("insurance_policy_num").max_length
        )
    )
    emerg_contact_name=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("emerg_contact_name").max_length
        )
    )
    emerg_contact_phone=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("emerg_contact_phone").max_length
        )
    )
    emerg_contact_relation=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("emerg_contact_relation").max_length
        )
    )
    consents_emerg_med_treatment=forms.ChoiceField(
        choices=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("consents_emerg_med_treatment").choices
        )
    )
    date=forms.DateField()
    signature=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("signature").max_length
        )
    )
