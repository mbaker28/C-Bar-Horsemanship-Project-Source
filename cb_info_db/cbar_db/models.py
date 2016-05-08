# Uses the following hack to support composite keys:
#    http://stackoverflow.com/questions/28712848/composite-primary-key-in-django

# TODO:
# Update ERD with changes herein:
#   EvalRidingExercises table
#       -Add holds_reins_*
#       -Add can_post_canter
#   Medication table
#       -Add participant_id as a FK
#       -Change PK to (medication_name, participant_id)
#   MedicalInfo table
#       -Add allergies_conditions_that_exclude_description
#       -Add physical_or_mental_issues_affecting_riding_description
#       -Add restriction_for_horse_activity_last_five_years_description
#   SeizureType table
#       -Add table
#   SeizureEval table
#       -Add FK to SeizureType to replace type_of_seizure
#       -Add during_seizure_* attribrutes
#       -Add can_communicate_when_will_occur attribute
#   AdaptationsNeeded table
#       -Remove assisted_device
#       -Remove mobility (duplicate of ambulatory_status)
#       -Remove num_sidewalker_* attributes
#   Sidewalker
#       -Add table


from math import floor
from django.db import models
from django.contrib.auth.models import User
from localflavor.us.models import USStateField
from localflavor.us.models import PhoneNumberField
from localflavor.us.models import USZipCodeField

# Global Constants and Choices
NAME_LENGTH=75
SHORT_ANSWER_LENGTH=100

MALE="M"
FEMALE="F"
GENDER_CHOICES=(
    (MALE, "Male"),
    (FEMALE, "Female")
)

MINOR="M"
ADULT_WITH_GUARDIAN="G"
ADULT_WITHOUT_GUARDIAN="A"
MINOR_STATUS_CHOICES=(
    (MINOR, "Minor"),
    (ADULT_WITH_GUARDIAN, "Adult with guardian"),
    (ADULT_WITHOUT_GUARDIAN, "Independent adult")
)

YES="Y"
NO="N"
YES_NO_CHOICES=(
    (YES, "Yes"),
    (NO, "No")
)
SOME="S"
YES_NO_SOME_CHOICES=(
    (YES, "Yes"),
    (NO, "No"),
    (SOME, "Some")
)
IMPAIRED="I"
YES_NO_IMPAIRED_CHOICES=(
    (YES, "Yes"),
    (NO, "No"),
    (IMPAIRED, "Impaired")
)

NULL_GAY=2 # anything that's not 1 or 0
TRUE_GAY=1 # Ryan ___
FALSE_GAY=0
YES_NO_NULL_BOOL_CHOICES=(
    (TRUE_GAY, "Yes"),
    (FALSE_GAY, "No"),
    (NULL_GAY, "Unknown")
)

UNSATISFACTORY="U"
POOR="P"
FAIR="F"
GOOD="G"
EXCELLENT="E"
NOT_PERFORMED_DISABILITY="N"
ATTEMPTS="A"
PARTIALLY_COMPLETES="C"
LIKERT_LIKE_CHOICES=(
    (UNSATISFACTORY, "Unsatisfactory"),
    (POOR, "Poor"),
    (FAIR, "Fair"),
    (GOOD, "Good"),
    (EXCELLENT, "Excellent"),
    (NOT_PERFORMED_DISABILITY, "Rider not able to perform due to disability"),
    (ATTEMPTS, "Attempts"),
    (PARTIALLY_COMPLETES, "Partially completes")
)
LIKERT_LIKE_CHOICES_NO_PC=(
    (UNSATISFACTORY, "Unsatisfactory"),
    (POOR, "Poor"),
    (FAIR, "Fair"),
    (GOOD, "Good"),
    (EXCELLENT, "Excellent"),
    (NOT_PERFORMED_DISABILITY, "Rider not able to perform due to disability"),
    (ATTEMPTS, "Attempts")
)
LIKERT_LIKE_CHOICES_MINIMAL=(
    (POOR, "Poor"),
    (FAIR, "Fair"),
    (GOOD, "Good")
)

CONSENT="Y"
NO_CONSENT="N"
CONSENT_CHOICES=(
    (CONSENT, "consent"),
    (NO_CONSENT, "do not consent")
)

ONE="1"
TWO="2"
THREE="3"
UNKNOWN="-"
ONE_TWO_THREE_CHOICES=(
    (ONE, "1"),
    (TWO, "2"),
    (THREE, "3"),
    (UNKNOWN, "N/A")
)

INDPENDENT="I"
MIN_ASSISTANCE="M"
FULL_ASSISTANCE="F"
ASSISTANCE_CHOICES=(
    (INDPENDENT, "Independent"),
    (MIN_ASSISTANCE, "Minimal assistance"),
    (FULL_ASSISTANCE, "Full assistance")
)
NOT_APPLICABLE="N"
ASSISTANCE_CHOICES_NA=(
    (INDPENDENT, "Independent"),
    (MIN_ASSISTANCE, "Minimal asst."),
    (FULL_ASSISTANCE, "Full asst."),
    (NOT_APPLICABLE, "n/a")
)

class Participant(models.Model):
    LEFT="L"
    RIGHT="R"
    AMBIDEXTROUS="A"
    NO_HAND_USE="N"
    HAND_CHOICES=(
        (LEFT, "Left"),
        (RIGHT, "Right"),
        (AMBIDEXTROUS, "Ambidextrous"),
        (NO_HAND_USE, "No meaningful hand use")
    )

    def __str__(self):
        return self.name + " (" + str(self.birth_date) + ")"

    participant_id=models.AutoField(primary_key=True) # Auto generated PK
    name=models.CharField(max_length=NAME_LENGTH)
    birth_date=models.DateField()
    email=models.EmailField() # Auto-validation for email addresses
    weight=models.DecimalField(max_digits=4, decimal_places=1) # Ex: 999.9
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES) # Ex: "M", "F"
    guardian_name=models.CharField(max_length=NAME_LENGTH)
    height=models.DecimalField(max_digits=4, decimal_places=1) # Ex: 999.9
    minor_status=models.CharField(max_length=1, choices=MINOR_STATUS_CHOICES)
    address_street=models.CharField(max_length=150)
    address_city=models.CharField(max_length=50)
    address_state=USStateField()
    address_zip=USZipCodeField()
    phone_home=PhoneNumberField()
    phone_cell=PhoneNumberField()
    phone_work=PhoneNumberField()
    school_institution=models.CharField(max_length=150, blank=True)
    handedness=models.CharField(
        max_length=1,
        choices=HAND_CHOICES,
        null=True
    )

    @property
    def height_in_feet_and_inches(self):
        """ Converts the value stored in the model's height field to a ft'in"
         styled string. """

        feet=floor(self.height / 12)
        inches=self.height % 12
        return str(feet) + "' " + str(inches) + "\""


class Caregiver(models.Model):
    caregiver_ID=models.AutoField(primary_key=True) # Auto generated PK
    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    name=models.CharField(max_length=NAME_LENGTH)
    phone=PhoneNumberField()


class Session(models.Model):
    session_ID=models.AutoField(primary_key=True) # Auto generated PK
    date=models.DateTimeField()
    tack=models.CharField(max_length=250, null=True)


class SessionPlanInd(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    horse_leader=models.CharField(max_length=NAME_LENGTH, null=True)


class SessionGoals(models.Model):
    GOAL_SHORT_TERM="S"
    GOAL_LONG_TERM="L"
    GOAL_CHOICES=(
        (GOAL_SHORT_TERM, "Short term goal"),
        (GOAL_LONG_TERM, "Long term goal")
    )
    class Meta: # Sets up PK as (participant_id, session_id)
        unique_together=(("participant_id", "session_id"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    session_id=models.ForeignKey(Session, on_delete=models.CASCADE)
    goal_type=models.CharField(max_length=1, choices=GOAL_CHOICES)
    goal_description=models.CharField(max_length=500)
    motivation=models.CharField(max_length=250)


class PhysRelease(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    health_provider_name=models.CharField(max_length=NAME_LENGTH)
    health_provider_title=models.CharField(max_length=50)
    health_provider_address=models.CharField(max_length=255)
    health_provider_phone=PhoneNumberField()
    health_provider_signature=models.CharField(max_length=NAME_LENGTH)
    #health_provider_license_num length is based on National Provider Identifier
    health_provider_license_num=models.CharField(max_length=10)


class Donor(models.Model):
    donor_id=models.AutoField(primary_key=True) # Auto generated PK
    name=models.CharField(max_length=NAME_LENGTH)
    email=models.EmailField()


class Horse(models.Model):
    horse_id=models.AutoField(primary_key=True) # Auto generated PK
    name=models.CharField(max_length=NAME_LENGTH)
    description=models.CharField(max_length=500)


class Donation(models.Model):
    DONATION_ADOPT_HORSE="H"
    DONATION_ADOPT_PARTICIPANT="P"
    DONATION_MONETARY="M"
    DONATION_CHOICES=(
        (DONATION_ADOPT_HORSE, "Horse adoption"),
        (DONATION_ADOPT_PARTICIPANT, "Participant adoption"),
        (DONATION_MONETARY, "Monetary donation")
    )

    donation_id=models.AutoField(primary_key=True) # Auto generated PK
    donor_id=models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        null=True
    )
    horse_id=models.ForeignKey(
        Horse,
        on_delete=models.CASCADE,
        null=True
    )
    participant_id=models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        null=True
    )
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    donation_type=models.CharField(max_length=1, choices=DONATION_CHOICES)
    purpose=models.CharField(max_length=SHORT_ANSWER_LENGTH, null=True)
    date=models.DateField(auto_now_add=True)


class Grouping(models.Model):
    """ AKA Class... reserved words and such """
    class_id=models.AutoField(primary_key=True) # Auto generated PK
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500)


class ObservationEvaluation(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    class_id=models.ForeignKey(Grouping, null=True, on_delete=models.SET_NULL)


class ParticipantType(models.Model):
    PARTICIPANT="P"
    VOLUNTEER="V"
    STAFF="S"
    TYPE_CHOICES=(
        (PARTICIPANT, "Participant"),
        (VOLUNTEER, "Volunteer"),
        (STAFF, "Staff")
    )

    class Meta:  # Sets up PK as (participant_id, participant_type)
        unique_together=(("participant_id","participant_type"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    participant_type=models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
    )


class Diagnosis(models.Model):
    PRIMARY="P"
    SECONDARY="S"
    DIAGNOSIS_CHOICES=(
        (PRIMARY, "Primary"),
        (SECONDARY, "Secondary")
    )

    class Meta: # Sets up PK as (participant_id, diagnosis)
        unique_together=(("participant_id","diagnosis"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    diagnosis=models.CharField(max_length=255)
    diagnosis_type=models.CharField(
        max_length=1,
        choices=DIAGNOSIS_CHOICES,
    )


class MediaRelease(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    consent=models.CharField(max_length=1, choices=CONSENT_CHOICES)
    signature=models.CharField(max_length=NAME_LENGTH)


class LiabilityRelease(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    signature=models.CharField(max_length=NAME_LENGTH)


class BackgroundCheck(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    signature=models.CharField(max_length=NAME_LENGTH)
    driver_license_num=models.CharField(max_length=18)


class ConfidentialityPolicy(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    agreement=models.CharField(max_length=1, choices=YES_NO_CHOICES)


class AuthorizeEmergencyMedicalTreatment(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()

    pref_medical_facility=models.CharField(max_length=70)
    insurance_provider=models.CharField(max_length=70)
    insurance_policy_num=models.CharField(max_length=20)
    emerg_contact_name=models.CharField(max_length=NAME_LENGTH)
    emerg_contact_phone=PhoneNumberField()
    emerg_contact_relation=models.CharField(max_length=50)
    alt_emerg_procedure=models.CharField(max_length=500, null=True)
    consents_emerg_med_treatment=models.CharField(
        max_length=1,
        choices=CONSENT_CHOICES
    )
    signature=models.CharField(max_length=NAME_LENGTH)


class EvalHorsemanship(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    rules_and_reasons=models.NullBooleanField()
    parts_of_horse=models.NullBooleanField()
    parts_of_saddle_english=models.NullBooleanField()
    parts_of_saddle_western=models.NullBooleanField()
    parts_of_bridle_english=models.NullBooleanField()
    parts_of_bridle_western=models.NullBooleanField()
    approach_tied_horse=models.NullBooleanField()
    methods_of_tying=models.NullBooleanField()
    halter=models.NullBooleanField()
    lead=models.NullBooleanField()
    groom=models.NullBooleanField()
    can_saddle_horse_english=models.NullBooleanField()
    can_saddle_horse_western=models.NullBooleanField()
    can_bridle_horse_english=models.NullBooleanField()
    can_bridle_horse_western=models.NullBooleanField()


class EvalAttitude(models.Model):
    WILLING="A"
    WILLING_NEEDS_ENCOURAGEMENT="B"
    UNWILLING="C"
    MOTIVATED_WELL="D"
    MOTIVATED_SOMEWHAT="E"
    NOT_MOTIVATED="F"
    SMILES_APPEARS_HAPPY="G"
    APPREHENSIVE="H"
    ATTITUDE_CHOICES=(
        (WILLING, "Willing"),
        (WILLING_NEEDS_ENCOURAGEMENT, "Willing, but needs encouragement"),
        (UNWILLING, "Unwilling"),
        (MOTIVATED_WELL, "Well motivated"),
        (MOTIVATED_SOMEWHAT, "Somewhat motivated"),
        (NOT_MOTIVATED, "Not motivated"),
        (SMILES_APPEARS_HAPPY, "Smiles, appears happy"),
        (APPREHENSIVE, "Apprehensive about the whole thing")
    )

    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()

    # 1/2/3/- choices:
    walking_through_barn_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    walking_through_barn_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    walking_through_barn_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    looking_at_horses_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    looking_at_horses_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    looking_at_horses_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    petting_horses_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    petting_horses_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    petting_horses_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    up_down_ramp_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    up_down_ramp_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    up_down_ramp_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    mounting_before_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    mounting_before_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    mounting_before_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    mounting_after_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    mounting_after_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    mounting_after_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    riding_before_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    riding_before_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    riding_before_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    riding_during_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    riding_during_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    riding_during_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    riding_after_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    riding_after_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    riding_after_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    understands_directions_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    understands_directions_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    understands_directions_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    participates_exercises_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    participates_exercises_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    participates_exercises_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    participates_games_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    participates_games_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    participates_games_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )

    general_attitude_willing=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    general_attitude_motivated=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )
    general_attitude_appearance=models.CharField(
        max_length=1,
        choices=ONE_TWO_THREE_CHOICES,
        default="-"
    )


    # Likert like choices w/o PARTIALLY_COMPLETES:
    comprehension=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES_NO_PC,
        blank=True
    )
    confidence=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES_NO_PC,
        blank=True
    )
    attention=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES_NO_PC,
        blank=True
    )
    relaxation=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES_NO_PC,
        blank=True
    )


class EvalRidingExercises(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()

    # Long-answer:
    comments=models.CharField(max_length=500, null=True)

    # Yes/No/Null choices:
    basic_trail_rules=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    basic_trail_rules_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    mount=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    mount_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    dismount=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    dismount_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    emergency_dismount=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    emergency_dismount_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    four_natural_aids=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    four_natural_aids_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    basic_control=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    basic_control_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    reverse_at_walk=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    reverse_at_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    reverse_at_trot=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    reverse_at_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    never_ridden=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    never_ridden_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    seat_at_walk=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    seat_at_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    seat_at_trot=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    seat_at_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    seat_at_canter=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    seat_at_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    basic_seat_english=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    basic_seat_english_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    basic_seat_western=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    basic_seat_western_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    hand_pos_english=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    hand_pos_english_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    hand_post_western=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    hand_post_western_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    two_point_trot=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    two_point_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    circle_trot_no_stirrups=models.NullBooleanField(
        choices=YES_NO_NULL_BOOL_CHOICES
    )
    circle_trot_no_stirrups_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    circle_at_canter=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    circle_at_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    circle_canter_no_stirrups=models.NullBooleanField(
        choices=YES_NO_NULL_BOOL_CHOICES
    )
    circle_canter_no_stirrups_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    two_point_canter=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    two_point_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    circle_at_walk=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    circle_at_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    circle_at_trot=models.NullBooleanField(choices=YES_NO_NULL_BOOL_CHOICES)
    circle_at_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    # Likert like choices:
    holds_handhold_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_handhold_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    holds_handhold_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_handhold_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    holds_handhold_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_handhold_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    holds_handhold_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_handhold_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    # MISSING FROM ERD !!!!!!!!!!!!!!

    holds_reins_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_reins_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    holds_reins_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_reins_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    holds_reins_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_reins_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    holds_reins_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_reins_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    # END MISSING FROM ERD

    shorten_lengthen_reins_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    shorten_lengthen_reins_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    shorten_lengthen_reins_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    shorten_lengthen_reins_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    shorten_lengthen_reins_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    shorten_lengthen_reins_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    shorten_lengthen_reins_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    shorten_lengthen_reins_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_control_horse_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_control_horse_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_control_horse_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_control_horse_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_control_horse_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_control_horse_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_control_horse_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_control_horse_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_halt_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_halt_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_halt_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_halt_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_halt_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_halt_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_halt_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_halt_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    drop_pickup_stirrups_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    drop_pickup_stirrups_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    drop_pickup_stirrups_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    drop_pickup_stirrups_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    drop_pickup_stirrups_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    drop_pickup_stirrups_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    drop_pickup_stirrups_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    drop_pickup_stirrups_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    rides_no_stirrups_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    rides_no_stirrups_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    rides_no_stirrups_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    rides_no_stirrups_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    rides_no_stirrups_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    rides_no_stirrups_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    rides_no_stirrups_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    rides_no_stirrups_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    maintain_half_seat_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    maintain_half_seat_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    maintain_half_seat_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    maintain_half_seat_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    maintain_half_seat_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    maintain_half_seat_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    maintain_half_seat_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    maintain_half_seat_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_post_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_post_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_post_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_post_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_post_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_post_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_post_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_post_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    proper_diagonal_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_diagonal_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    proper_diagonal_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_diagonal_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    proper_diagonal_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_diagonal_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    proper_diagonal_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_diagonal_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    proper_lead_canter_sees=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_lead_canter_sees_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    proper_lead_canter_knows=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_lead_canter_knows_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_steer_over_cavalletti_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_steer_over_cavalletti_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_steer_over_cavalletti_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_steer_over_cavalletti_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_steer_over_cavalletti_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_steer_over_cavalletti_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    can_steer_over_cavalletti_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_steer_over_cavalletti_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    jump_crossbar_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    jump_crossbar_walk_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    jump_crossbar_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    jump_crossbar_sit_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    jump_crossbar_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    jump_crossbar_post_trot_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    jump_crossbar_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    jump_crossbar_canter_com=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

class EvalPhysical(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()

    # Likert like choices:
    arms_head_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    arms_head_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    arms_side_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    arms_side_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_tail_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_talk_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    twist_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    twist_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_ears_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_ears_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    arm_circle_back_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    arm_circle_back_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    arm_circle_fwd_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    arm_circle_fwd_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    hand_circle_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    hand_circle_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_right_tow_w_left_hand_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_right_tow_w_left_hand_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_left_tow_w_right_hand_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_left_tow_w_right_hand_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_both_toes_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    touch_both_toes_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    swing_legs_back_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    swing_legs_back_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    swing_legs_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    swing_legs_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    stand_in_stirrups_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    stand_in_stirrups_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    bend_foot_up_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    bend_foot_up_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    bend_foot_down_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    bend_foot_down_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    foot_circles_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    foot_circles_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    lie_back_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    lie_back_halt=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )

    # Likert like choices w/o PARTIALLY_COMPLETES:
    balance=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES_NO_PC,
        blank=True
    )
    coordination=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES_NO_PC,
        blank=True
    )


class MedicalInfo(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    physical_release=models.ForeignKey(
        PhysRelease,
        null=True,
        on_delete=models.SET_NULL
    )

    primary_physician_name=models.CharField(max_length=NAME_LENGTH)
    primary_physician_phone=PhoneNumberField()
    last_seen_by_physician_date=models.DateField()
    last_seen_by_physician_reason=models.CharField(max_length=250)
    allergies_conditions_that_exclude=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    allergies_conditions_that_exclude_description=models.CharField(
        max_length=500,
        null=True
    )
    heat_exhaustion_stroke=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    tetanus_shot_last_ten_years=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    seizures_last_six_monthes=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    doctor_concered_re_horse_activites=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    physical_or_mental_issues_affecting_riding=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    physical_or_mental_issues_affecting_riding_description=models.CharField(
        max_length=500,
        null=True
    )
    restriction_for_horse_activity_last_five_years=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    restriction_for_horse_activity_last_five_years_description=models.CharField(
        max_length=500,
        null=True
    )
    present_restrictions_for_horse_activity=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    ) # If yes -> PhysRelease required
    limiting_surgeries_last_six_monthes=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    limiting_surgeries_last_six_monthes_description=models.CharField(
        max_length=500,
        null=True
    )
    signature=models.CharField(max_length=NAME_LENGTH)
    currently_taking_any_medication=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    pregnant=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )


class Medication(models.Model):
    class Meta: # Sets up PK as (participant_id, date, medication_name)
        unique_together=(("participant_id", "date", "medication_name"))

    participant_id=models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
    )
    date=models.DateField()
    medication_name=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
    )

    reason_taken=models.CharField(max_length=50)
    frequency=models.CharField(max_length=50)


class SeizureEval(models.Model):
    SEIZURE_GRAND="G"
    SEIZURE_PETITE="P"
    SEIZURE_CONTROLLED="C"
    SEIZURE_NONE="N"
    SEIZURE_TYPES=(
        (SEIZURE_GRAND, "Grand"),
        (SEIZURE_PETITE, "Petite"),
        (SEIZURE_CONTROLLED, "Controlled"),
        (SEIZURE_NONE, "None")
    )


    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()
    type_of_seizure=models.CharField(
        max_length=1,
        choices=SEIZURE_TYPES
    )
    date_of_last_seizure=models.DateField()
    duration_of_last_seizure=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    typical_cause=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    seizure_indicators=models.CharField(max_length=500)
    after_effect=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    during_seizure_stare=models.NullBooleanField()
    during_seizure_stare_length=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    during_seizure_walks=models.NullBooleanField()
    during_seizure_aimless=models.NullBooleanField()
    during_seizure_cry_etc=models.NullBooleanField()
    during_seizure_bladder_bowel=models.NullBooleanField()
    during_seizure_confused_etc=models.NullBooleanField()
    during_seizure_other=models.NullBooleanField()
    during_seizure_other_description=models.CharField(max_length=500, null=True)
    knows_when_will_occur=models.NullBooleanField()
    can_communicate_when_will_occur=models.NullBooleanField()
    action_to_take_do_nothing=models.NullBooleanField()
    action_to_take_dismount=models.NullBooleanField()
    action_to_take_allow_time=models.NullBooleanField()
    action_to_take_allow_time_how_long=models.DecimalField(
        max_digits=2,
        decimal_places=0,
        null=True
    )
    action_to_take_report_immediately=models.NullBooleanField()
    action_to_take_send_note=models.NullBooleanField()
    seizure_frequency=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    signature=models.CharField(max_length=NAME_LENGTH)


# DISABLED: We are no longer storing seizuretype records.
# DO NOT REMOVE Until after 5/2/16 demonstration, if given go ahead.
# class SeizureType(models.Model):
#     class Meta: # Sets up PK as (seizure_eval, name)
#         unique_together=(("seizure_eval","name"))
#
#     seizure_eval=models.ForeignKey(SeizureEval, on_delete=models.CASCADE)
#     name=models.CharField(max_length=50)


class AdaptationsNeeded(models.Model):
    WALKS_IND="I"
    IND_WITH_CANE_ETC="C"
    WHEELCHAIR_MIN_NO_ASSISTANCE="N"
    WHEELCHAIR_FULL_ASSISTANCE="A"
    OTHER="O"
    AMBULATORY_CHOICES=(
        (WALKS_IND, "Walks independently"),
        (IND_WITH_CANE_ETC, "Independent with cane/bronco/walker"),
        (WHEELCHAIR_MIN_NO_ASSISTANCE, "Wheelchair with minimal or no assistance"),
        (WHEELCHAIR_FULL_ASSISTANCE, "Wheelchair with full assistance"),
        (OTHER, "Other") # -> ambulatory_status_other needed
    )

    MNT_PORT_BLOCK="P"
    MNT_STATIC_BLOCK="S"
    MNT_RAMP="R"
    MOUNT_DEVICE_CHOICES=(
        (MNT_PORT_BLOCK, "Portable block"),
        (MNT_STATIC_BLOCK, "Static block"),
        (MNT_RAMP, "Ramp")
    )

    MNT_OVER_CREST="T"
    MNT_OVER_CROUP="P"
    MOUNT_TYPE_CHOICES=(
        (MNT_OVER_CREST, "Over crest"),
        (MNT_OVER_CROUP, "Over croup")
    )

    DMT_OVER_CROUP="A"
    DMT_OVER_CROUP_LF_STIRRUP="B"
    DMT_OVER_CREST="C"
    DISMOUNT_TYPE_CHOICES=(
        (DMT_OVER_CROUP, "Over croup"),
        (DMT_OVER_CROUP_LF_STIRRUP, "Over croup with left foot in stirrup"),
        (DMT_OVER_CREST, "Over crest")
    )

    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()

    mount_assistance_required=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES
    )
    mount_device_needed=models.CharField(
        max_length=1,
        choices=MOUNT_DEVICE_CHOICES,
        null=True
    )
    mount_type=models.CharField(
        max_length=1,
        choices=MOUNT_TYPE_CHOICES,
        null=True
    )

    dismount_assistance_required=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES
    )
    dismount_type=models.CharField(
        max_length=1,
        choices=DISMOUNT_TYPE_CHOICES
    )
    posture_standing=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    posture_sitting=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    posture_mounted=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    ambulatory_status=models.CharField(max_length=1, choices=AMBULATORY_CHOICES)
    ambulatory_status_other=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )

    gait_flat=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_uneven=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_incline=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_decline=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_stairs=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_balance=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_standing_up=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_sitting_down=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_straddle_up=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    gait_straddle_down=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )

    # Sidewalker information for initial assessment
    num_sidewalkers_walk_spotter=models.DecimalField(
        max_digits=1,
        decimal_places=0
    )
    num_sidewalkers_walk_heel_hold=models.DecimalField(
        max_digits=1,
        decimal_places=0
    )
    num_sidewalkers_walk_over_thigh=models.DecimalField(
        max_digits=1,
        decimal_places=0
    )
    num_sidewalkers_walk_other=models.DecimalField(
        max_digits=1,
        decimal_places=0
    )
    num_sidewalkers_trot_spotter=models.DecimalField(
        max_digits=1,
        decimal_places=0
    )
    num_sidewalkers_trot_heel_hold=models.DecimalField(
        max_digits=1,
        decimal_places=0
    )
    num_sidewalkers_trot_over_thigh=models.DecimalField(
        max_digits=1,
        decimal_places=0
    )
    num_sidewalkers_trot_other=models.DecimalField(
        max_digits=1,
        decimal_places=0
    )


class Sidewalker(models.Model):
    """ Sidewalker information on a per-session basis. """

    SPOTTER="S"
    HEELHOLD="H"
    OVER_THIGH="T"
    OTHER="O"
    SIDEWALKER_POSITION_CHOICES=(
        (SPOTTER, "Spotter"),
        (HEELHOLD, "Heel hold"),
        (OVER_THIGH, "Over thigh"),
        (OTHER, "Other")
    )

    # The sidewalker:
    volunteer_id=models.ForeignKey(
        Participant,
        related_name="volunteer",
        on_delete=models.SET_NULL,
        null=True
    )
    # The participant that needs sidewalker:
    student_id=models.ForeignKey(
        Participant,
        related_name="student",
        on_delete=models.CASCADE
    )

    session_id=models.ForeignKey(Session, on_delete=models.CASCADE)

    sidewalker_pace=models.CharField(
        max_length=1,
        choices=(
            ("W", "Walk"),
            ("T", "Trot")
        )
    )
    sidewalker_position=models.CharField(
        max_length=1,
        choices=SIDEWALKER_POSITION_CHOICES
    )
    sidewalker_position_other_description=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )


class AuthorizedUser(models.Model):
    """ Links to the built in Django authentication system. Acts as a bridge
     from the User model in Django auth to Participant in our models. """

    class Meta: # Sets up PK as (participant_id, authorized_user_id)
        unique_together=(("participant_id","authorized_user_id"))

    participant_id=models.ForeignKey(Participant)
    authorized_user_id = models.OneToOneField(User)


class IntakeAssessment(models.Model):
    NO_ISSUES="N"
    DO_NOT_TOUCH="T"
    LIGHT_TOUCH="L"
    DEEP_PRESSURE="P"
    TACTILE_ISSUE_CHOICES=(
        (NO_ISSUES, "No tactile issues"),
        (DO_NOT_TOUCH, "Don't touch me!"),
        (LIGHT_TOUCH, "Light touch"),
        (DEEP_PRESSURE, "Deep pressure")
    )

    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField()

    staff_reviewed_medical_info=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    staff_reviewed_medical_info_date=models.DateField()
    precautions=models.CharField(max_length=500)
    impulsive=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    eye_contact=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    attention_span=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES_MINIMAL,
    )
    interacts_with_others=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES
    )
    communication_verbal=models.CharField(
        max_length=1,
        choices=YES_NO_IMPAIRED_CHOICES,
        null=True
    )
    communication_verbal_comments=models.CharField(
        max_length=SHORT_ANSWER_LENGTH
    )
    language_skills_signs=models.CharField(
        max_length=1,
        choices=YES_NO_SOME_CHOICES,
        null=True
    )
    language_skills_comments=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    visual_impaired=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        null=True
    )
    visual_comments=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    hearing_impaired=models.CharField(
        max_length=1,
        choices=YES_NO_CHOICES,
        null=True
    )
    hearing_comments=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    tactile=models.CharField(
        max_length=1,
        choices=TACTILE_ISSUE_CHOICES,
        null=True
    )
    tactile_comments=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    motor_skills_gross_left=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    motor_skills_gross_right=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    motor_skills_fine_left=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    motor_skills_fine_right=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    motor_skills_comments=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    # motor skills: hand dominance is in Participant model.
    posture_forward_halt=models.NullBooleanField()
    posture_forward_walk=models.NullBooleanField()
    posture_back_halt=models.NullBooleanField()
    posture_back_walk=models.NullBooleanField()
    posture_center_halt=models.NullBooleanField()
    posture_center_walk=models.NullBooleanField()
    posture_chairseat_halt=models.NullBooleanField()
    posture_chairseat_walk=models.NullBooleanField()
    posture_aligned_halt=models.NullBooleanField()
    posture_aligned_walk=models.NullBooleanField()

    rein_use_hold_halt=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    rein_use_steer_left_right_halt=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    rein_use_hold_walk=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    rein_use_steer_left_right_walk=models.CharField(
        max_length=1,
        choices=ASSISTANCE_CHOICES_NA,
        default=NOT_APPLICABLE,
        null=True
    )
    mounted_comments=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    risk_benefit_comments=models.CharField(max_length=500)
