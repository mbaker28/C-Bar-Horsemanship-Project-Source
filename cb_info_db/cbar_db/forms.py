from datetime import date
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import RadioSelect
from cbar_db import models
import logging
from localflavor.us.forms import USStateField
from localflavor.us.forms import USPhoneNumberField
from localflavor.us.forms import USZipCodeField


ERROR_TEXT_NO_PHONE="Please enter at least one phone number."

# Set the years available for date dropdowns to the last 125 years:
this_year=date.today().year
YEARS=range(this_year-125, this_year+1)


loggeyMcLogging=logging.getLogger(__name__)


class ApplicationForm(forms.Form):
    FEET_MIN=2
    FEET_MAX=6
    INCH_MIN=0
    INCH_MAX=11.9
    ERROR_TEXT_INVALID_HEIGHT_FT=(
        "Must be between " + str(FEET_MIN) + " and " + str(FEET_MAX) + "."
    )
    ERROR_TEXT_INVALID_HEIGHT_IN=(
        "Must be between " + str(INCH_MIN) + " and " + str(INCH_MAX) + "."
    )

    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )

    birth_date=forms.DateField(widget=SelectDateWidget(years=YEARS))

    height_feet=forms.DecimalField(
        max_digits=1,
        decimal_places=0
    )

    height_inches=forms.DecimalField(
        max_digits=3,
        decimal_places=1
    )

    weight=forms.DecimalField(
        max_digits=models.Participant._meta.get_field("weight").max_digits,
        decimal_places=models.Participant._meta.get_field("weight").decimal_places
    )

    gender=forms.ChoiceField(
        #max_length=models.Participant._meta.get_field("gender").max_length,
        choices=models.Participant._meta.get_field("gender").choices
    )

    minor_status=forms.ChoiceField(
        #max_length=models.Participant._meta.get_field("minor_status").max_length,
        choices=models.Participant._meta.get_field("minor_status").choices
    )

    school_institution=forms.CharField(
        max_length=models.Participant._meta.get_field("school_institution").max_length
    )

    guardian_name=forms.CharField(
        max_length=models.Participant._meta.get_field("guardian_name").max_length,
        required=False
    )

    address_street=forms.CharField(
        max_length=models.Participant._meta.get_field("address_street").max_length
    )

    address_city=forms.CharField(
        max_length=models.Participant._meta.get_field("address_city").max_length
    )

    address_state=USStateField()

    address_zip=USZipCodeField()

    phone_home=USPhoneNumberField(required=False)

    phone_cell=USPhoneNumberField(required=False)

    phone_work=USPhoneNumberField(required=False)

    email=forms.EmailField()

    def clean(self):
        """ Automatically called when .is_valid() or .clean() is called. """

        cleaned_data=super(ApplicationForm, self).clean()
        phone_home=cleaned_data.get("phone_home")
        phone_cell=cleaned_data.get("phone_cell")
        phone_work=cleaned_data.get("phone_work")
        height_feet=cleaned_data.get("height_feet")
        height_inches=cleaned_data.get("height_inches")

        # Verify that the user entered at least one phone number:
        if phone_home == "" and phone_cell == "" and phone_work == "":
            # The user hasn't entered at least one phone number, so the form is
            # invalid. Raise errors for each phone field:
            self.add_error("phone_home", ERROR_TEXT_NO_PHONE)
            self.add_error("phone_cell", ERROR_TEXT_NO_PHONE)
            self.add_error("phone_work", ERROR_TEXT_NO_PHONE)

        # DEBUGGING:
        loggeyMcLogging.error("height_feet == " + str(height_feet))
        loggeyMcLogging.error("height_inches == " + str(height_inches))

        # Verify that the user entered a valid height in the feet field:
        if height_feet > self.FEET_MAX or height_feet < self.FEET_MIN:
            self.add_error("height_feet", self.ERROR_TEXT_INVALID_HEIGHT_FT)

        # Verify that the user entered a valid height in the inches field:
        if height_inches > self.INCH_MAX or height_inches < self.INCH_MIN:
            self.add_error("height_inches", self.ERROR_TEXT_INVALID_HEIGHT_IN)


class SeizureEvaluationForm(forms.Form):
    name=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("name").max_length
        )
    )

    birth_date=forms.DateField(widget=SelectDateWidget(years=YEARS))

    date=forms.DateField(
        widget=SelectDateWidget(years=YEARS),
        initial=date.today()
    )

    guardian_name=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("guardian_name").max_length
        )
    )

    phone_home=USPhoneNumberField(required=False)

    phone_cell=USPhoneNumberField(required=False)

    phone_work=USPhoneNumberField(required=False)

    type_of_seizure=forms.ChoiceField(
        choices=models.SeizureEval._meta.get_field("type_of_seizure").choices,
        initial="N"
    )

    date_of_last_seizure=forms.DateField(widget=SelectDateWidget(years=YEARS))

    seizure_frequency=forms.CharField(max_length=(models.SeizureEval
            ._meta.get_field("seizure_frequency").max_length
        )
    )

    duration_of_last_seizure=forms.CharField(max_length=(models.SeizureEval
            ._meta.get_field("duration_of_last_seizure").max_length
        )
    )
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

    medication_one_name=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("medication_name").max_length
        ),
        required=False
    )
    medication_one_reason=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("reason_taken").max_length
        ),
        required=False
    )
    medication_one_frequency=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("frequency").max_length
        ),
        required=False
    )

    medication_two_name=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("medication_name").max_length
        ),
        required=False
    )
    medication_two_reason=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("reason_taken").max_length
        ),
        required=False
    )
    medication_two_frequency=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("frequency").max_length
        ),
        required=False
    )

    medication_three_name=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("medication_name").max_length
        ),
        required=False
    )
    medication_three_reason=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("reason_taken").max_length
        ),
        required=False
    )
    medication_three_frequency=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("frequency").max_length
        ),
        required=False
    )

    during_seizure_stare=forms.BooleanField(required=False)

    during_seizure_stare_length=forms.CharField(max_length=(models.SeizureEval
            ._meta.get_field("during_seizure_stare_length").max_length
        ),
        required=False
    )

    during_seizure_walks=forms.BooleanField(required=False)

    during_seizure_aimless=forms.BooleanField(required=False)

    during_seizure_cry_etc=forms.BooleanField(required=False)

    during_seizure_bladder_bowel=forms.BooleanField(required=False)

    during_seizure_confused_etc=forms.BooleanField(required=False)

    during_seizure_other=forms.BooleanField(required=False)

    during_seizure_other_description=forms.CharField(
        max_length=(models.SeizureEval._meta
            .get_field("during_seizure_other_description").max_length
        ),
        required=False
    )

    knows_when_will_occur=forms.BooleanField(required=False)
    can_communicate_when_will_occur=forms.BooleanField(required=False)
    action_to_take_do_nothing=forms.BooleanField(required=False)
    action_to_take_dismount=forms.BooleanField(required=False)
    action_to_take_allow_time=forms.BooleanField(required=False)
    action_to_take_allow_time_how_long=forms.DecimalField(
        max_digits=2,
        decimal_places=0,
        required=False
    )
    action_to_take_report_immediately=forms.BooleanField(required=False)
    action_to_take_send_note=forms.BooleanField(required=False)

    signature=forms.CharField(
        max_length=(models.SeizureEval._meta
            .get_field("signature").max_length
        )
    )

    def clean(self):
        """ Automatically called when .is_valid() or .clean() is called. """

        cleaned_data=super(SeizureEvaluationForm, self).clean()
        phone_home=cleaned_data.get("phone_home")
        phone_cell=cleaned_data.get("phone_cell")
        phone_work=cleaned_data.get("phone_work")

        # Verify that the user entered at least one phone number
        if phone_home == "" and phone_cell == "" and phone_work == "":
            # The user hasn't entered at least one phone number, so the form is
            # invalid. Raise errors for each phone field:

            self.add_error("phone_home", ERROR_TEXT_NO_PHONE)
            self.add_error("phone_cell", ERROR_TEXT_NO_PHONE)
            self.add_error("phone_work", ERROR_TEXT_NO_PHONE)


class LiabilityReleaseForm(forms.Form):
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )

    birth_date=forms.DateField(widget=SelectDateWidget(years=YEARS))

    signature=forms.CharField(
        max_length=models.LiabilityRelease._meta.get_field("signature").max_length
    )
    date=forms.DateField(
        widget=SelectDateWidget(years=YEARS),
        initial=date.today()
    )


class MedicalReleaseForm(forms.Form):
    primary_physician_name=forms.CharField(
        max_length=(models.MedicalInfo._meta
            .get_field("primary_physician_name").max_length
        )
    )

    primary_physician_phone=USPhoneNumberField()

    last_seen_by_physician_date=forms.DateField(widget=SelectDateWidget(years=YEARS))

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
    medication_one_reason=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("reason_taken").max_length
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
    medication_two_reason=forms.CharField(
        max_length=(models.Medication._meta
            .get_field("reason_taken").max_length
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

    birth_date=forms.DateField(widget=SelectDateWidget(years=YEARS))

    signature=forms.CharField(
        max_length=models.MedicalInfo._meta.get_field("signature").max_length
    )

    date=forms.DateField(
        widget=SelectDateWidget(years=YEARS),
        initial=date.today()
    )


class BackgroundCheckForm(forms.Form):
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )
    signature=forms.CharField(
        max_length=(models.BackgroundCheck._meta
            .get_field("signature").max_length
        )
    )
    date=forms.DateField(
        widget=SelectDateWidget(years=YEARS),
        initial=date.today()
    )
    birth_date=forms.DateField(widget=SelectDateWidget(years=YEARS))
    driver_license_num=forms.CharField(
        max_length=(models.BackgroundCheck._meta
            .get_field("driver_license_num").max_length
        )
    )


class MediaReleaseForm(forms.Form):
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )
    birth_date=forms.DateField(widget=SelectDateWidget(years=YEARS))
    consent=forms.ChoiceField(
        choices=models.MediaRelease._meta.get_field("consent").choices
    )
    signature=forms.CharField(
        max_length=models.MediaRelease._meta.get_field("signature").max_length
    )
    date=forms.DateField(
        widget=SelectDateWidget(years=YEARS),
        initial=date.today()
    )


class EmergencyMedicalReleaseForm(forms.Form):
    # Stored in Participant
    name=forms.CharField(
        max_length=models.Participant._meta.get_field("name").max_length
    )
    birth_date=forms.DateField(widget=SelectDateWidget(years=YEARS))

    # Stored in MedicalInfo
    primary_physician_name=forms.CharField(
        max_length=(models.MedicalInfo._meta
            .get_field("primary_physician_name").max_length
        )
    )
    primary_physician_phone=USPhoneNumberField()

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
    emerg_contact_phone=USPhoneNumberField()
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
    date=forms.DateField(
        widget=SelectDateWidget(years=YEARS),
        initial=date.today()
    )
    signature=forms.CharField(
        max_length=(models.AuthorizeEmergencyMedicalTreatment._meta
            .get_field("signature").max_length
        )
    )



class RiderEvalChecklistForm(forms.Form):
    comments=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("comments").max_length
        )
    )

    date=forms.DateField(widget=SelectDateWidget(years=YEARS))

    basic_trail_rules=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("basic_trail_rules").choices)

    mount=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("mount").choices)

    dismount=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("dismount").choices)

    emergency_dismount=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("emergency_dismount").choices)

    four_natural_aids=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("four_natural_aids").choices)

    basic_control=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("basic_control").choices)

    reverse_at_walk=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("reverse_at_walk").choices)

    reverse_at_trot=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("reverse_at_trot").choices)

    never_ridden=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("never_ridden").choices)

    seat_at_walk=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("seat_at_walk").choices)

    seat_at_trot=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("seat_at_trot").choices)

    seat_at_canter=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("seat_at_canter").choices)

    basic_seat_english=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("basic_seat_english").choices)

    basic_seat_western=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("basic_seat_western").choices)

    hand_pos_english=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("hand_pos_english").choices)

    hand_post_western=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("hand_post_western").choices)

    two_point_trot=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("two_point_trot").choices)

    circle_trot_no_stirrups=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("circle_trot_no_stirrups").choices)

    circle_at_canter=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("circle_at_canter").choices)

    circle_canter_no_stirrups=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("circle_canter_no_stirrups").choices)

    two_point_canter=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("two_point_canter").choices)

    circle_at_walk=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("circle_at_walk").choices)

    circle_at_trot=forms.ChoiceField(widget=RadioSelect,
        choices=models.EvalRidingExercises._meta
            .get_field("circle_at_trot").choices)

    holds_handhold_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_handhold_walk").choices
        )
    )

    holds_handhold_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_handhold_sit_trot").choices
        )
    )

    holds_handhold_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_handhold_post_trot").choices
        )
    )

    holds_handhold_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_handhold_canter").choices
        )
    )

    holds_reins_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_reins_walk").choices
        )
    )

    holds_reins_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_reins_sit_trot").choices
        )
    )

    holds_reins_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_reins_post_trot").choices
        )
    )

    holds_reins_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_reins_canter").choices
        )
    )

    holds_reins_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("holds_reins_canter").choices
        )
    )

    shorten_lengthen_reins_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("shorten_lengthen_reins_walk").choices
        )
    )

    shorten_lengthen_reins_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("shorten_lengthen_reins_sit_trot").choices
        )
    )

    shorten_lengthen_reins_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("shorten_lengthen_reins_post_trot").choices
        )
    )

    shorten_lengthen_reins_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("shorten_lengthen_reins_canter").choices
        )
    )

    can_control_horse_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_control_horse_walk").choices
        )
    )

    can_control_horse_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_control_horse_sit_trot").choices
        )
    )

    can_control_horse_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_control_horse_post_trot").choices
        )
    )

    can_control_horse_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_control_horse_canter").choices
        )
    )

    can_halt_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_halt_walk").choices
        )
    )

    can_halt_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_halt_sit_trot").choices
        )
    )

    can_halt_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_halt_post_trot").choices
        )
    )

    can_halt_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_halt_canter").choices
        )
    )

    drop_pickup_stirrups_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("drop_pickup_stirrups_walk").choices
        )
    )

    drop_pickup_stirrups_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("drop_pickup_stirrups_sit_trot").choices
        )
    )

    drop_pickup_stirrups_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("drop_pickup_stirrups_post_trot").choices
        )
    )

    drop_pickup_stirrups_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("drop_pickup_stirrups_canter").choices
        )
    )

    rides_no_stirrups_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("rides_no_stirrups_walk").choices
        )
    )

    rides_no_stirrups_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("rides_no_stirrups_sit_trot").choices
        )
    )

    rides_no_stirrups_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("rides_no_stirrups_post_trot").choices
        )
    )

    rides_no_stirrups_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("rides_no_stirrups_canter").choices
        )
    )

    maintain_half_seat_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("maintain_half_seat_walk").choices
        )
    )

    maintain_half_seat_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("maintain_half_seat_sit_trot").choices
        )
    )

    maintain_half_seat_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("maintain_half_seat_post_trot").choices
        )
    )

    maintain_half_seat_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("maintain_half_seat_canter").choices
        )
    )

    can_post_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_post_walk").choices
        )
    )

    can_post_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_post_sit_trot").choices
        )
    )

    can_post_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_post_post_trot").choices
        )
    )

    can_post_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_post_canter").choices
        )
    )

    proper_diagonal_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("proper_diagonal_walk").choices
        )
    )

    proper_diagonal_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("proper_diagonal_sit_trot").choices
        )
    )

    proper_diagonal_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("proper_diagonal_post_trot").choices
        )
    )

    proper_diagonal_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("proper_diagonal_canter").choices
        )
    )

    proper_lead_canter_sees=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("proper_lead_canter_sees").choices
        )
    )

    proper_lead_canter_knows=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("proper_lead_canter_knows").choices
        )
    )

    can_steer_over_cavalletti_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_steer_over_cavalletti_walk").choices
        )
    )

    can_steer_over_cavalletti_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_steer_over_cavalletti_sit_trot").choices
        )
    )

    can_steer_over_cavalletti_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_steer_over_cavalletti_post_trot").choices
        )
    )

    can_steer_over_cavalletti_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("can_steer_over_cavalletti_canter").choices
        )
    )

    jump_crossbar_walk=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("jump_crossbar_walk").choices
        )
    )

    jump_crossbar_sit_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("jump_crossbar_sit_trot").choices
        )
    )

    jump_crossbar_post_trot=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("jump_crossbar_post_trot").choices
        )
    )

    jump_crossbar_canter=forms.ChoiceField(widget=RadioSelect,
        choices=(models.EvalRidingExercises._meta
            .get_field("jump_crossbar_canter").choices
        )
    )


class ParticipantAdoptionForm(forms.Form):
    amount=forms.DecimalField(
        max_digits=models.Donation._meta.get_field("amount").max_digits,
        decimal_places=models.Donation._meta.get_field("amount").decimal_places
    )
    name=forms.CharField(
        max_length=models.Donor._meta.get_field("name").max_length
    )
    email=forms.EmailField()


class HorseAdoptionForm(forms.Form):
    amount=forms.DecimalField(
        max_digits=models.Donation._meta.get_field("amount").max_digits,
        decimal_places=models.Donation._meta.get_field("amount").decimal_places
    )
    name=forms.CharField(
        max_length=models.Donor._meta.get_field("name").max_length
    )
    email=forms.EmailField()



class MonetaryDonationForm(forms.Form):
    amount=forms.DecimalField(
        max_digits=models.Donation._meta.get_field("amount").max_digits,
        decimal_places=models.Donation._meta.get_field("amount").decimal_places
    )
    name=forms.CharField(
        max_length=models.Donor._meta.get_field("name").max_length
    )
    email=forms.EmailField()
