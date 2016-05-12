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
        max_length=models.Participant._meta.get_field("school_institution").max_length,
        required=False
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
        choices=models.SeizureEval._meta.get_field("type_of_seizure").choices
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
    name=forms.CharField(
        max_length=(models.Participant._meta
            .get_field("name").max_length
        )
    )
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
    pregnant=forms.ChoiceField(
        choices=(models.MedicalInfo._meta
            .get_field("pregnant").choices
        )
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


class RiderIntakeAssessmentForm(forms.Form):
    # Primary document sources:
    #   -"Volunteer Folder/.../blank/Rider Intake Assessment (Spring 2014).pdf"
    #   -"Volunteer Folder/.../Rider Intake Assessment (Spring 2014).pdf"

    # GAAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRR
    # participant_id_index=forms.CharField(
    #     max_length=1000,
    #     widget=forms.HiddenInput,
    #     initial="Burp"
    # )

    # Stored in AdaptationsNeeded:
    posture_standing=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta
            .get_field("posture_standing").choices
        ),
        widget=RadioSelect
    )
    posture_sitting=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta
            .get_field("posture_sitting").choices
        ),
        widget=RadioSelect
    )
    posture_mounted=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta
            .get_field("posture_mounted").choices
        ),
        widget=RadioSelect
    )
    ambulatory_status=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta
            .get_field("ambulatory_status").choices
        )
    )
    ambulatory_status_other=forms.CharField(
        max_length=(
            models.AdaptationsNeeded._meta
            .get_field("ambulatory_status_other").max_length
        ),
        required=False
    )
    gait_flat=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_flat").choices
        ),
        widget=RadioSelect
    )
    gait_uneven=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_uneven").choices
        ),
        widget=RadioSelect
    )
    gait_incline=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_incline").choices
        ),
        widget=RadioSelect
    )
    gait_decline=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_decline").choices
        ),
        widget=RadioSelect
    )
    gait_stairs=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_stairs").choices
        ),
        widget=RadioSelect
    )
    gait_balance=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_balance").choices
        ),
        widget=RadioSelect
    )
    gait_standing_up=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_standing_up")
            .choices
        ),
        widget=RadioSelect
    )
    gait_sitting_down=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_sitting_down")
            .choices
        ),
        widget=RadioSelect
    )
    gait_straddle_up=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_straddle_up")
            .choices
        ),
        widget=RadioSelect
    )
    gait_straddle_down=forms.ChoiceField(
        choices=(
            models.AdaptationsNeeded._meta.get_field("gait_straddle_down")
            .choices
        ),
        widget=RadioSelect
    )

    # Stored in SeizureEval (should auto-fill)
    # type_of_seizure=forms.ChoiceField(
    #     choices=models.SeizureEval._meta.get_field("type_of_seizure").choices
    # )

    # Stored in Diagnosis:
    # primary_diagnosis=forms.CharField( # Should be auto-filled if applicable
    #     max_length=models.Diagnosis._meta.get_field("diagnosis").max_length
    # )

    # Stored in AuthorizedUser (?):
    # assessor_name=forms.CharField(
    #     max_length=models.Participant._meta.get_field("name").max_length
    # )

    # Stored in IntakeAssessment:
    staff_reviewed_medical_info=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta
            .get_field("staff_reviewed_medical_info").choices
        )
    )
    staff_reviewed_medical_info_date=forms.DateField(
        widget=SelectDateWidget(years=YEARS)
    )
    impulsive=forms.ChoiceField(
        choices=models.IntakeAssessment._meta.get_field("impulsive").choices,
        widget=RadioSelect
    )
    eye_contact=forms.ChoiceField(
        choices=models.IntakeAssessment._meta.get_field("eye_contact").choices,
        widget=RadioSelect
    )
    attention_span=forms.ChoiceField(
        choices=models.IntakeAssessment._meta.get_field("attention_span").choices,
        widget=RadioSelect
    )
    interacts_with_others=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("interacts_with_others")
            .choices
        ),
        widget=RadioSelect
    )
    communication_verbal=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("communication_verbal")
            .choices
        ),
        widget=RadioSelect,
        required=False
    )
    language_skills_signs=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("language_skills_signs")
            .choices
        ),
        widget=RadioSelect
    )
    visual_impaired=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("visual_impaired")
            .choices
        ),
        widget=RadioSelect
    )
    visual_comments=forms.CharField(
        max_length=(
            models.IntakeAssessment._meta.get_field("visual_comments")
            .max_length
        ),
        required=False
    )
    hearing_impaired=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("hearing_impaired")
            .choices
        ),
        widget=RadioSelect
    )
    hearing_comments=forms.CharField(
        max_length=(
            models.IntakeAssessment._meta.get_field("hearing_comments")
            .max_length
        ),
        required=False
    )
    tactile=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("tactile")
            .choices
        ),
        widget=RadioSelect
    )
    tactile_comments=forms.CharField(
        max_length=(
            models.IntakeAssessment._meta.get_field("tactile_comments")
            .max_length
        ),
        required=False
    )
    motor_skills_gross_left=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("motor_skills_gross_left")
            .choices
        ),
        widget=RadioSelect
    )
    motor_skills_gross_right=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("motor_skills_gross_right")
            .choices
        ),
        widget=RadioSelect
    )
    motor_skills_fine_left=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("motor_skills_fine_left")
            .choices
        ),
        widget=RadioSelect
    )
    motor_skills_fine_right=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("motor_skills_fine_right")
            .choices
        ),
        widget=RadioSelect
    )
    motor_skills_comments=forms.CharField(
        max_length=(
            models.IntakeAssessment._meta.get_field("motor_skills_comments")
            .max_length
        ),
        required=False
    )
    posture_forward_halt=forms.BooleanField(required=False)
    posture_forward_walk=forms.BooleanField(required=False)
    posture_back_halt=forms.BooleanField(required=False)
    posture_back_walk=forms.BooleanField(required=False)
    posture_center_halt=forms.BooleanField(required=False)
    posture_center_walk=forms.BooleanField(required=False)
    posture_chairseat_halt=forms.BooleanField(required=False)
    posture_chairseat_walk=forms.BooleanField(required=False)
    posture_aligned_halt=forms.BooleanField(required=False)
    posture_aligned_walk=forms.BooleanField(required=False)
    rein_use_hold_halt=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("motor_skills_fine_right")
            .choices
        ),
        widget=RadioSelect
    )
    rein_use_steer_left_right_halt=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("motor_skills_fine_right")
            .choices
        ),
        widget=RadioSelect
    )
    rein_use_hold_walk=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("motor_skills_fine_right")
            .choices
        ),
        widget=RadioSelect
    )
    rein_use_steer_left_right_walk=forms.ChoiceField(
        choices=(
            models.IntakeAssessment._meta.get_field("motor_skills_fine_right")
            .choices
        ),
        widget=RadioSelect
    )
    mounted_comments=forms.CharField(
        max_length=(
            models.IntakeAssessment._meta.get_field("mounted_comments")
            .max_length
        ),
        required=False
    )
    risk_benefit_comments=forms.CharField(
        max_length=(
            models.IntakeAssessment._meta.get_field("risk_benefit_comments")
            .max_length
        ),
        widget=forms.Textarea(attrs={'rows':4, 'cols':40}),
        required=False
    )
    goals_expectations=forms.CharField(
        max_length=(
            models.IntakeAssessment._meta.get_field("goals_expectations")
            .max_length
        ),
        widget=forms.Textarea(attrs={'rows':4, 'cols':40}),
        required=False
    )


class ObservationEvaluation(forms.Form):
    # name=forms.CharField(
    #     max_length=models.Participant._meta.get_field("name").max_length
    # )
    date=forms.DateField(widget=SelectDateWidget, initial=date.today())

    walking_through_barn_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "walking_through_barn_willing"
        ).choices
    )
    walking_through_barn_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "walking_through_barn_motivated"
        ).choices
    )
    walking_through_barn_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "walking_through_barn_appearance"
        ).choices
    )

    looking_at_horses_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "looking_at_horses_willing"
        ).choices
    )
    looking_at_horses_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "looking_at_horses_motivated"
        ).choices
    )
    looking_at_horses_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "looking_at_horses_appearance"
        ).choices
    )

    petting_horses_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "petting_horses_willing"
        ).choices
    )
    petting_horses_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "petting_horses_motivated"
        ).choices
    )
    petting_horses_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "petting_horses_appearance"
        ).choices
    )

    up_down_ramp_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "up_down_ramp_willing"
        ).choices
    )
    up_down_ramp_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "up_down_ramp_motivated"
        ).choices
    )
    up_down_ramp_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "up_down_ramp_appearance"
        ).choices
    )

    mounting_before_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "mounting_before_willing"
        ).choices
    )
    mounting_before_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "mounting_before_motivated"
        ).choices
    )
    mounting_before_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "mounting_before_appearance"
        ).choices
    )

    mounting_after_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "mounting_after_willing"
        ).choices
    )
    mounting_after_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "mounting_after_motivated"
        ).choices
    )
    mounting_after_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "mounting_after_appearance"
        ).choices
    )

    riding_before_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_before_willing"
        ).choices
    )
    riding_before_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_before_motivated"
        ).choices
    )
    riding_before_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_before_appearance"
        ).choices
    )

    riding_during_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_during_willing"
        ).choices
    )
    riding_during_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_during_motivated"
        ).choices
    )
    riding_during_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_during_appearance"
        ).choices
    )

    riding_after_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_after_willing"
        ).choices
    )
    riding_after_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_after_motivated"
        ).choices
    )
    riding_after_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "riding_after_appearance"
        ).choices
    )

    understands_directions_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "understands_directions_willing"
        ).choices
    )
    understands_directions_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "understands_directions_motivated"
        ).choices
    )
    understands_directions_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "understands_directions_appearance"
        ).choices
    )

    participates_exercises_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "participates_exercises_willing"
        ).choices
    )
    participates_exercises_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "participates_exercises_motivated"
        ).choices
    )
    participates_exercises_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "participates_exercises_appearance"
        ).choices
    )

    participates_games_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "participates_games_willing"
        ).choices
    )
    participates_games_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "participates_games_motivated"
        ).choices
    )
    participates_games_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "participates_games_appearance"
        ).choices
    )

    general_attitude_willing=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "general_attitude_willing"
        ).choices
    )
    general_attitude_motivated=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "general_attitude_motivated"
        ).choices
    )
    general_attitude_appearance=forms.ChoiceField(
        widget=RadioSelect,
        initial="-",
        choices=models.EvalAttitude._meta.get_field(
            "general_attitude_appearance"
        ).choices
    )


class SessionPlanForm(forms.Form):
    # Stored in Participant
    # name=forms.CharField(
    #     max_length=models.Participant._meta.get_field("name").max_length
    # )
    # birth_date=forms.DateField()

    # Stored in Session
    date=forms.DateField(
        widget=SelectDateWidget(years=YEARS),
        initial=date.today()
    )

    # Stored in SessionPlanInd
    horse_leader=forms.CharField(
        max_length=models.SessionPlanInd
        ._meta.get_field("horse_leader").max_length
    )

    # Stored in SessionGoals
    goal_type=forms.ChoiceField(
        #max_length=models.SessionGoals._meta.get_field("goal_type").max_length,
        choices=models.SessionGoals._meta.get_field("goal_type").choices
    )
    goal_description=forms.CharField(
        max_length=models.SessionGoals
        ._meta.get_field("goal_description").max_length
    )
    motivation=forms.CharField(
        max_length=models.SessionGoals._meta.get_field("motivation").max_length
    )

    # Stored in Horse
    horse_name=forms.CharField(
        max_length=models.Horse._meta.get_field("name").max_length
    )
    # description=forms.CharField(
    #     max_length=models.Horse._meta.get_field("description").max_length
    # )

    # Stored in Diagnosis
    # diagnosis=forms.CharField(
    #     max_length=models.Diagnosis._meta.get_field("diagnosis").max_length
    # )
    # diagnosis_type=forms.ChoiceField(
    #     choices=models.Diagnosis._meta.get_field("diagnosis_type").choices
    # )

    # Stored in AdaptationsNeeded
    ambulatory_status=forms.ChoiceField(
        choices=models.AdaptationsNeeded
        ._meta.get_field("ambulatory_status").choices
    )
    ambulatory_status_other=forms.CharField(
        max_length=models.AdaptationsNeeded
        ._meta.get_field("ambulatory_status_other").max_length,
        required=False
    )
    mount_assistance_required=forms.ChoiceField(
        choices=models.AdaptationsNeeded
        ._meta.get_field("mount_assistance_required").choices
    )
    mount_device_needed=forms.ChoiceField(
        choices=models.AdaptationsNeeded
        ._meta.get_field("mount_device_needed").choices,
        required=False
    )
    mount_type=forms.ChoiceField(
        choices=models.AdaptationsNeeded._meta.get_field("mount_type").choices,
        required=False
    )
    dismount_assistance_required=forms.ChoiceField(
        choices=models.AdaptationsNeeded
        ._meta.get_field("dismount_assistance_required").choices
    )
    dismount_type=forms.ChoiceField(
        choices=models.AdaptationsNeeded
        ._meta.get_field("dismount_type").choices
    )
    num_sidewalkers_walk_spotter=forms.DecimalField(
        max_digits=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_walk_spotter").max_digits,
        decimal_places=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_walk_spotter").decimal_places
    )
    num_sidewalkers_walk_heel_hold=forms.DecimalField(
        max_digits=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_walk_heel_hold").max_digits,
        decimal_places=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_walk_heel_hold").decimal_places
    )
    num_sidewalkers_walk_over_thigh=forms.DecimalField(
        max_digits=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_walk_over_thigh").max_digits,
        decimal_places=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_walk_over_thigh").decimal_places
    )
    num_sidewalkers_walk_other=forms.DecimalField(
        max_digits=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_walk_other").max_digits,
        decimal_places=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_walk_other").decimal_places
    )
    num_sidewalkers_trot_spotter=forms.DecimalField(
        max_digits=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_trot_spotter").max_digits,
        decimal_places=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_trot_spotter").decimal_places
    )
    num_sidewalkers_trot_heel_hold=forms.DecimalField(
        max_digits=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_trot_heel_hold").max_digits,
        decimal_places=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_trot_heel_hold").decimal_places
    )
    num_sidewalkers_trot_over_thigh=forms.DecimalField(
        max_digits=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_trot_over_thigh").max_digits,
        decimal_places=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_trot_over_thigh").decimal_places
    )
    num_sidewalkers_trot_other=forms.DecimalField(
        max_digits=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_trot_other").max_digits,
        decimal_places=models.AdaptationsNeeded
        ._meta.get_field("num_sidewalkers_trot_other").decimal_places
    )


class RiderEvalChecklistForm(forms.Form):
    comments=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("comments").max_length),
            required=False
    )


    basic_trail_rules_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("basic_trail_rules_com").max_length
            ),
            required=False
    )

    mount_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("mount_com").max_length),
            required=False
    )

    dismount_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("dismount_com").max_length),
            required=False
    )

    emergency_dismount_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("emergency_dismount_com").max_length),
            required=False
    )

    four_natural_aids_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("four_natural_aids_com").max_length),
            required=False
    )

    basic_control_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("basic_control_com").max_length),
            required=False
    )

    reverse_at_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("reverse_at_walk_com").max_length),
            required=False
    )

    reverse_at_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("reverse_at_trot_com").max_length),
            required=False
    )

    never_ridden_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("never_ridden_com").max_length),
            required=False
    )

    seat_at_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("seat_at_walk_com").max_length),
            required=False
    )

    seat_at_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("seat_at_trot_com").max_length),
            required=False
    )

    seat_at_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("seat_at_canter_com").max_length),
            required=False
    )

    basic_seat_english_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("basic_seat_english_com").max_length),
            required=False
    )

    basic_seat_western_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("basic_seat_western_com").max_length),
            required=False
    )

    hand_pos_english_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("hand_pos_english_com").max_length),
            required=False
    )

    hand_post_western_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("hand_post_western_com").max_length),
            required=False
    )

    two_point_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("two_point_trot_com").max_length),
            required=False
    )

    circle_trot_no_stirrups_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("circle_trot_no_stirrups_com").max_length),
            required=False
    )

    circle_at_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("circle_at_canter_com").max_length),
            required=False
    )

    circle_canter_no_stirrups_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("circle_canter_no_stirrups_com").max_length),
            required=False
    )

    two_point_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("two_point_canter_com").max_length),
            required=False
    )

    circle_at_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("circle_at_walk_com").max_length),
            required=False
    )

    circle_at_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("circle_at_trot_com").max_length),
            required=False
    )

    holds_handhold_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("holds_handhold_walk_com").max_length),
            required=False
    )

    holds_handhold_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("holds_handhold_sit_trot_com").max_length),
            required=False
    )

    holds_handhold_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("holds_handhold_post_trot_com").max_length),
            required=False
    )

    holds_handhold_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("holds_handhold_canter_com").max_length),
            required=False
    )

    holds_reins_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("holds_reins_walk_com").max_length),
            required=False
    )

    holds_reins_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("holds_reins_sit_trot_com").max_length),
            required=False
    )

    holds_reins_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("holds_reins_post_trot_com").max_length),
            required=False
    )

    holds_reins_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("holds_reins_canter_com").max_length),
            required=False
    )

    shorten_lengthen_reins_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("shorten_lengthen_reins_walk_com").max_length),
            required=False
    )

    shorten_lengthen_reins_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("shorten_lengthen_reins_sit_trot_com").max_length),
            required=False
    )

    shorten_lengthen_reins_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("shorten_lengthen_reins_post_trot_com").max_length),
            required=False
    )

    shorten_lengthen_reins_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("shorten_lengthen_reins_canter_com").max_length),
            required=False
    )

    can_control_horse_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_control_horse_walk_com").max_length),
            required=False
    )

    can_control_horse_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_control_horse_sit_trot_com").max_length),
            required=False
    )

    can_control_horse_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_control_horse_post_trot_com").max_length),
            required=False
    )

    can_control_horse_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_control_horse_canter_com").max_length),
            required=False
    )

    can_halt_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_halt_walk_com").max_length),
            required=False
    )

    can_halt_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_halt_sit_trot_com").max_length),
            required=False
    )

    can_halt_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_halt_post_trot_com").max_length),
            required=False
    )

    can_halt_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_halt_canter_com").max_length),
            required=False
    )

    drop_pickup_stirrups_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("drop_pickup_stirrups_walk_com").max_length),
            required=False
    )

    drop_pickup_stirrups_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("drop_pickup_stirrups_sit_trot_com").max_length),
            required=False
    )

    drop_pickup_stirrups_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("drop_pickup_stirrups_post_trot_com").max_length),
            required=False
    )

    drop_pickup_stirrups_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("drop_pickup_stirrups_canter_com").max_length),
            required=False
    )

    rides_no_stirrups_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("rides_no_stirrups_walk_com").max_length),
            required=False
    )

    rides_no_stirrups_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("rides_no_stirrups_sit_trot_com").max_length),
            required=False
    )

    rides_no_stirrups_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("rides_no_stirrups_post_trot_com").max_length),
            required=False
    )

    rides_no_stirrups_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("rides_no_stirrups_canter_com").max_length),
            required=False
    )

    maintain_half_seat_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("maintain_half_seat_walk_com").max_length),
            required=False
    )

    maintain_half_seat_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("maintain_half_seat_sit_trot_com").max_length),
            required=False
    )

    maintain_half_seat_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("maintain_half_seat_post_trot_com").max_length),
            required=False
    )

    maintain_half_seat_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("maintain_half_seat_canter_com").max_length),
            required=False
    )

    can_post_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_post_walk_com").max_length),
            required=False
    )

    can_post_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_post_sit_trot_com").max_length),
            required=False
    )

    can_post_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_post_post_trot_com").max_length),
            required=False
    )

    can_post_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_post_canter_com").max_length),
            required=False
    )

    proper_diagonal_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("proper_diagonal_walk_com").max_length),
            required=False
    )

    proper_diagonal_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("proper_diagonal_sit_trot_com").max_length),
            required=False
    )

    proper_diagonal_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("proper_diagonal_post_trot_com").max_length),
            required=False
    )

    proper_diagonal_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("proper_diagonal_canter_com").max_length),
            required=False
    )

    proper_lead_canter_sees_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("proper_lead_canter_sees_com").max_length),
            required=False
    )

    proper_lead_canter_knows_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("proper_lead_canter_knows_com").max_length),
            required=False
    )

    can_steer_over_cavalletti_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_steer_over_cavalletti_walk_com").max_length),
            required=False
    )

    can_steer_over_cavalletti_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_steer_over_cavalletti_sit_trot_com").max_length),
            required=False
    )

    can_steer_over_cavalletti_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_steer_over_cavalletti_post_trot_com").max_length),
            required=False
    )

    can_steer_over_cavalletti_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("can_steer_over_cavalletti_canter_com").max_length),
            required=False
    )

    jump_crossbar_walk_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("jump_crossbar_walk_com").max_length),
            required=False
    )

    jump_crossbar_sit_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("jump_crossbar_sit_trot_com").max_length),
            required=False
    )

    jump_crossbar_post_trot_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("jump_crossbar_post_trot_com").max_length),
            required=False
    )

    jump_crossbar_canter_com=forms.CharField(
        max_length=(models.EvalRidingExercises._meta
            .get_field("jump_crossbar_canter_com").max_length),
            required=False
    )

    date=forms.DateField(
        widget=SelectDateWidget(years=YEARS),
        initial=date.today()
    )

    basic_trail_rules=forms.NullBooleanField(widget=RadioSelect(
            choices=models.EvalRidingExercises._meta
            .get_field("basic_trail_rules").choices),
            required=False)

    mount=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("mount").choices),
            required=False)

    dismount=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("dismount").choices),
            required=False)

    emergency_dismount=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("emergency_dismount").choices),
            required=False)

    four_natural_aids=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("four_natural_aids").choices),
            required=False)

    basic_control=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("basic_control").choices),
            required=False)

    reverse_at_walk=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("reverse_at_walk").choices),
            required=False)

    reverse_at_trot=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("reverse_at_trot").choices),
            required=False)

    never_ridden=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("never_ridden").choices),
            required=False)

    seat_at_walk=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("seat_at_walk").choices),
            required=False)

    seat_at_trot=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("seat_at_trot").choices),
            required=False)

    seat_at_canter=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("seat_at_canter").choices),
            required=False)

    basic_seat_english=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("basic_seat_english").choices),
            required=False)

    basic_seat_western=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("basic_seat_western").choices),
            required=False)

    hand_pos_english=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("hand_pos_english").choices),
            required=False)

    hand_post_western=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("hand_post_western").choices),
            required=False)

    two_point_trot=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("two_point_trot").choices),
            required=False)

    circle_trot_no_stirrups=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("circle_trot_no_stirrups").choices),
            required=False)

    circle_at_canter=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("circle_at_canter").choices),
            required=False)

    circle_canter_no_stirrups=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("circle_canter_no_stirrups").choices),
            required=False)

    two_point_canter=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("two_point_canter").choices),
            required=False)

    circle_at_walk=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("circle_at_walk").choices),
            required=False)

    circle_at_trot=forms.NullBooleanField(widget=RadioSelect(
        choices=models.EvalRidingExercises._meta
            .get_field("circle_at_trot").choices),
            required=False)

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
    purpose=forms.CharField(
        max_length=models.Donation._meta.get_field("purpose").max_length,
        required=False
    ) # Git is being a butt...
