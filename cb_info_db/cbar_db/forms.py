from django import forms
from cbar_db import models

class SeizureEvaluationForm(forms.Form):
    name=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("name").max_length
        )
    )

    date=forms.DateField()

    guardian_name=forms.CharField(
        max_length=(models.Participant._meta
            .get_field)("guardian_name").max_length
        )
    )

    phone_home=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("phone_home").max_length
        )
    )

    phone_cell_work=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("phone_cell_work").max_length
        )
    )

    #do I need two of the phone_cell_work.....

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

    #may need a boolean field in the models.py

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

    signature=forms.CharField(
        max_length=(models.SeizureEval._meta
            .get_field("signature").max_length
        )
    )

    date=forms.DateField()

    #C-Bar staff signature needed in models.py

    date=forms.DateField()
