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


from django.db import models
from django.contrib.auth.models import User

# Global Constants and Choices
NAME_LENGTH=75
PHONE_LENGTH=15
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

YES_BOOL=True
NO_BOOL=False
YES_NO_BOOL_CHOICES=(
    (YES_BOOL, "Yes"),
    (NO_BOOL, "No")
)

UNSATISFACTORY="U"
POOR="P"
FAIR="F"
GOOD="G"
EXCELLENT="E"
NOT_PERFORMED_DISABILITY="N"
ATTEMPTS="A"
PARTIALLY_COMPLETES="P"
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

CONSENT="Y"
NO_CONSENT="N"
CONSENT_CHOICES=(
    (CONSENT, "consent"),
    (NO_CONSENT, "do not consent")
)

class Participant(models.Model):
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
    address_zip=models.CharField(max_length=6)
    phone_home=models.CharField(max_length=PHONE_LENGTH)
    phone_cell=models.CharField(max_length=PHONE_LENGTH)
    phone_work=models.CharField(max_length=PHONE_LENGTH)
    school_institution=models.CharField(max_length=150, blank=True)
    #date=models.DateField(primary_key=True)
    # signature=models.CharField(max_length=NAME_LENGTH)


class Caregiver(models.Model):
    caregiver_ID=models.AutoField(primary_key=True) # Auto generated PK
    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    name=models.CharField(max_length=NAME_LENGTH)
    phone=models.CharField(max_length=PHONE_LENGTH)


class Session(models.Model):
    class Meta:  # Sets up PK as (session_id, date)
        unique_together=(("session_ID", "date"))
    session_ID=models.AutoField(primary_key=True) # Auto generated PK
    date=models.DateTimeField()
    tack=models.CharField(max_length=250)


class SessionGoals(models.Model):
    GOAL_SHORT_TERM="S"
    GOAL_LONG_TERM="L"
    GOAL_CHOICES=(
        (GOAL_SHORT_TERM, "Short term goal"),
        (GOAL_LONG_TERM, "Long term goal")
    )
    class Meta: # Sets up PK as (participant_id, session_id)
        unique_together=(("participant_id", "session_id"))

    session_goals_id=models.AutoField(primary_key=True) # Auto generated PK
    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    session_id=models.ForeignKey(Session, on_delete=models.CASCADE)
    goal_type=models.CharField(max_length=1, choices=GOAL_CHOICES)
    goal_description=models.CharField(max_length=500)
    motiviation=models.CharField(max_length=250)


class PhysRelease(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    health_provider_name=models.CharField(max_length=NAME_LENGTH)
    health_provider_title=models.CharField(max_length=50)
    health_provider_address=models.CharField(max_length=255)
    health_provider_phone=models.CharField(max_length=PHONE_LENGTH)
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
    donor_id=models.ForeignKey(Donor, on_delete=models.CASCADE)
    horse_id=models.ForeignKey(Horse, on_delete=models.CASCADE)
    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    # Commented out because I don"t think we"ll actually store payment info,
    # but it"s in the ERD...
    # payment_info=models.CharField(max_length=500)
    donation_type=models.CharField(max_length=1, choices=DONATION_CHOICES)


class Grouping(models.Model):
    """ AKA Class... reserved words and such """
    class_id=models.AutoField(primary_key=True) # Auto generated PK
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500)


class ObservationEvaluation(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
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
        primary_key=True
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
    diagnosis=models.CharField(max_length=255, primary_key=True)
    diagnosis_type=models.CharField(
        max_length=1,
        choices=DIAGNOSIS_CHOICES,
    )


class MediaRelease(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    consent=models.CharField(max_length=1, choices=CONSENT_CHOICES)
    signature=models.CharField(max_length=NAME_LENGTH)


class LiabilityRelease(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    signature=models.CharField(max_length=NAME_LENGTH)


class BackgroundCheck(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    signature=models.CharField(max_length=NAME_LENGTH)
    driver_license_num=models.CharField(max_length=18)


class ConfidentialityPolicy(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    agreement=models.CharField(max_length=1, choices=YES_NO_CHOICES)


class AuthorizeEmergencyMedicalTreatment(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    pref_medical_facility=models.CharField(max_length=70)
    insurance_provider=models.CharField(max_length=70)
    insurance_policy_num=models.CharField(max_length=20)
    emerg_contact_name=models.CharField(max_length=NAME_LENGTH)
    emerg_contact_phone=models.CharField(max_length=PHONE_LENGTH)
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
    date=models.DateField(primary_key=True)
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
    date=models.DateField(primary_key=True)

    # Attiude choices:
    walking_through_barn=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    looking_at_horses=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    petting_horses=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    up_down_ramp=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    mounting_before=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    mounting_after=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    riding_before=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    riding_during=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    riding_after=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    understands_directions=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    participates_exercises=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    participates_games=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
    )
    general_attitude=models.CharField(
        max_length=1,
        choices=ATTITUDE_CHOICES,
        blank=True
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
    date=models.DateField(primary_key=True)

    # Long-answer:
    comments=models.CharField(max_length=500, null=True)

    # Yes/No/Null choices:
    basic_trail_rules=models.NullBooleanField()
    mount=models.NullBooleanField()
    dismount=models.NullBooleanField()
    emergency_dismount=models.NullBooleanField()
    four_natural_aids=models.NullBooleanField()
    basic_control=models.NullBooleanField()
    reverse_at_walk=models.NullBooleanField()
    reverse_at_trot=models.NullBooleanField()
    never_ridden=models.NullBooleanField()
    seat_at_walk=models.NullBooleanField()
    seat_at_trot=models.NullBooleanField()
    seat_at_canter=models.NullBooleanField()
    basic_seat_english=models.NullBooleanField()
    basic_seat_western=models.NullBooleanField()
    hand_pos_english=models.NullBooleanField()
    hand_post_western=models.NullBooleanField()
    two_point_trot=models.NullBooleanField()
    circle_trot_no_stirrups=models.NullBooleanField()
    circle_at_canter=models.NullBooleanField()
    circle_canter_no_stirrups=models.NullBooleanField()
    two_point_canter=models.NullBooleanField()
    circle_at_walk=models.NullBooleanField()
    circle_at_trot=models.NullBooleanField()

    # Likert like choices:
    holds_handhold_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_handhold_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_handhold_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_handhold_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    # MISSING FROM ERD !!!!!!!!!!!!!!
    holds_reins_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_reins_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_reins_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    holds_reins_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    # END MISSING FROM ERD
    shorten_lengthen_reins_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    shorten_lengthen_reins_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    shorten_lengthen_reins_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    shorten_lengthen_reins_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_control_horse_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_control_horse_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_control_horse_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_control_horse_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_halt_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_halt_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_halt_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_halt_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    drop_pickup_stirrups_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    drop_pickup_stirrups_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    drop_pickup_stirrups_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    drop_pickup_stirrups_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    rides_no_stirrups_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    rides_no_stirrups_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    rides_no_stirrups_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    rides_no_stirrups_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    maintain_half_seat_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    maintain_half_seat_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    maintain_half_seat_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    maintain_half_seat_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_post_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_post_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_post_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_post_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_diagonal_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_diagonal_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_diagonal_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_diagonal_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_lead_canter_sees=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    proper_lead_canter_knows=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_steer_over_cavalletti_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_steer_over_cavalletti_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_steer_over_cavalletti_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    can_steer_over_cavalletti_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    jump_crossbar_walk=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    jump_crossbar_sit_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    jump_crossbar_post_trot=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )
    jump_crossbar_canter=models.CharField(
        max_length=1,
        choices=LIKERT_LIKE_CHOICES,
        blank=True
    )


class EvalPhysical(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)

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
    date=models.DateField(primary_key=True)
    physical_release=models.ForeignKey(
        PhysRelease,
        null=True,
        on_delete=models.SET_NULL
    )

    primary_physician_name=models.CharField(max_length=NAME_LENGTH)
    primary_physician_phone=models.CharField(max_length=PHONE_LENGTH)
    last_seen_by_physician_date=models.DateField()
    last_seen_by_physician_reason=models.CharField(max_length=250)
    allergies_conditions_that_exclude=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )
    allergies_conditions_that_exclude_description=models.CharField(
        max_length=500,
        null=True
    )
    heat_exhaustion_stroke=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )
    tetanus_shot_last_ten_years=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )
    seizures_last_six_monthes=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )
    doctor_concered_re_horse_activites=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )
    physical_or_mental_issues_affecting_riding=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )
    physical_or_mental_issues_affecting_riding_description=models.CharField(
        max_length=500,
        null=True
    )
    restriction_for_horse_activity_last_five_years=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )
    restriction_for_horse_activity_last_five_years_description=models.CharField(
        max_length=500,
        null=True
    )
    present_restrictions_for_horse_activity=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    ) # If yes -> PhysRelease required
    limiting_surgeries_last_six_monthes=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )
    limiting_surgeries_last_six_monthes_description=models.CharField(
        max_length=500,
        null=True
    )
    signature=models.CharField(max_length=NAME_LENGTH)
    currently_taking_any_medication=models.BooleanField(
        choices=YES_NO_BOOL_CHOICES
    )


class Medication(models.Model):
    class Meta: # Sets up PK as (medical_info_id, medication_name)
        unique_together=(("medical_info_id","medication_name"))

    medical_info_id=models.ForeignKey(MedicalInfo, on_delete=models.CASCADE, null=True)
    medication_name=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        primary_key=True
    )

    duration_taken=models.CharField(max_length=25)
    frequency=models.CharField(max_length=25)


class SeizureEval(models.Model):

    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(("participant_id","date"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
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
        decimal_places=0
    )
    action_to_take_report_immediately=models.NullBooleanField()
    action_to_take_send_note=models.NullBooleanField()
    seizure_frequency=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    signature=models.CharField(max_length=NAME_LENGTH)


class SeizureType(models.Model):
    class Meta: # Sets up PK as (seizure_eval, name)
        unique_together=(("seizure_eval","name"))

    seizure_eval=models.ForeignKey(SeizureEval, on_delete=models.CASCADE)
    name=models.CharField(max_length=50, primary_key=True)


class AdaptationsNeeded(models.Model):
    INDPENDENT="I"
    MIN_ASSISTANCE="M"
    FULL_ASSISTANCE="F"
    ASSISTANCE_CHOICES=(
        (INDPENDENT, "Independent"),
        (MIN_ASSISTANCE, "Minimal assistance"),
        (FULL_ASSISTANCE, "Full assistance")
    )

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

    class Meta: # Sets up PK as (participant_id, adaptation_id)
        unique_together=(("participant_id","adaptation_id"))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    adaptation_id=models.AutoField(primary_key=True)

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
    posture_standing=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    posture_sitting=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    posture_mounted=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    ambulatory_status=models.CharField(max_length=1, choices=AMBULATORY_CHOICES)
    ambulatory_status_other=models.CharField(
        max_length=SHORT_ANSWER_LENGTH,
        null=True
    )
    gait_flat=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_uneven=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_incline=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_decline=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_stairs=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_balance=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_standing_up=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_standing_down=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_straddle_up=models.CharField(max_length=SHORT_ANSWER_LENGTH)
    gait_straddle_down=models.CharField(max_length=SHORT_ANSWER_LENGTH)

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
    authorized_user_id = models.OneToOneField(User, primary_key=True)
