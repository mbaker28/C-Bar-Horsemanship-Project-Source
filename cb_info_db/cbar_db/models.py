# Uses the following hack to support composite keys:
#    http://stackoverflow.com/questions/28712848/composite-primary-key-in-django

from django.db import models

# Constants and Choices
NAME_LENGTH=75
PHONE_LENGTH=15

MALE='M'
FEMALE='F'
GENDER_CHOICES=(
    (MALE, 'Male'),
    (FEMALE, 'Female')
)

MINOR='M'
ADULT_WITH_GUARDIAN='G'
ADULT_WITHOUT_GUARDIAN='A'
MINOR_STATUS_CHOICES=(
    (MINOR, 'Minor'),
    (ADULT_WITH_GUARDIAN, 'Adult with guardian'),
    (ADULT_WITHOUT_GUARDIAN, 'Independent adult')
)

YES='Y'
NO='N'
YES_NO_CHOICES=(
    (YES, 'Yes'),
    (NO, 'No')
)


class Participant(models.Model):
    participant_id=models.AutoField(primary_key=True) # Auto generated PK
    name=models.CharField(max_length=NAME_LENGTH)
    birth_date=models.DateField()
    email=models.EmailField() # Auto-validation for email addresses
    weight=models.DecimalField(max_digits=4, decimal_places=1) # Ex: 999.9
    gender=models.CharField(max_length=1, choices=GENDER_CHOICES) # Ex: 'M', 'F'
    guardian_name=models.CharField(max_length=NAME_LENGTH)
    height=models.DecimalField(max_digits=4, decimal_places=1) # Ex: 999.9
    minor_status=models.CharField(max_length=1, choices=MINOR_STATUS_CHOICES)
    address_street=models.CharField(max_length=150)
    address_city=models.CharField(max_length=50)
    address_zip=models.CharField(max_length=6)
    phone_home=models.CharField(max_length=PHONE_LENGTH)
    phone_cell_work=models.CharField(max_length=PHONE_LENGTH)
    school_institution=models.CharField(max_length=150, blank=True)


class Caregiver(models.Model):
    caregiver_ID=models.AutoField(primary_key=True) # Auto generated PK
    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    name=models.CharField(max_length=NAME_LENGTH)
    phone=models.CharField(max_length=PHONE_LENGTH)


class Session(models.Model):
    class Meta:  # Sets up PK as (session_id, date)
        unique_together=(('session_ID', 'date'))
    session_ID=models.AutoField(primary_key=True) # Auto generated PK
    date=models.DateTimeField()
    tack=models.CharField(max_length=250)


class SessionGoals(models.Model):
    GOAL_SHORT_TERM='S'
    GOAL_LONG_TERM='L'
    GOAL_CHOICES=(
        (GOAL_SHORT_TERM, 'Short term goal'),
        (GOAL_LONG_TERM, 'Long term goal')
    )
    class Meta: # Sets up PK as (participant_id, session_id)
        unique_together=(('participant_id', 'session_id'))

    session_goals_id=models.AutoField(primary_key=True) # Auto generated PK
    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    session_id=models.ForeignKey(Session, on_delete=models.CASCADE)
    goal_type=models.CharField(max_length=1, choices=GOAL_CHOICES)
    goal_description=models.CharField(max_length=500)
    motiviation=models.CharField(max_length=250)


class PhysRelease(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(('participant_id','date'))

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
    DONATION_ADOPT_HORSE='H'
    DONATION_ADOPT_PARTICIPANT='P'
    DONATION_MONETARY='M'
    DONATION_CHOICES=(
        (DONATION_ADOPT_HORSE, 'Horse adoption'),
        (DONATION_ADOPT_PARTICIPANT, 'Participant adoption'),
        (DONATION_MONETARY, 'Monetary donation')
    )

    donation_id=models.AutoField(primary_key=True) # Auto generated PK
    donor_id=models.ForeignKey(Donor, on_delete=models.CASCADE)
    horse_id=models.ForeignKey(Horse, on_delete=models.CASCADE)
    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    # Commented out because I don't think we'll actually store payment info,
    # but it's in the ERD...
    # payment_info=models.CharField(max_length=500)
    donation_type=models.CharField(max_length=1, choices=DONATION_CHOICES)


class Grouping(models.Model):
    """ AKA Class... reserved words and such """
    class_id=models.AutoField(primary_key=True) # Auto generated PK
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=500)


class ObservationEvaluation(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(('participant_id','date'))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    class_id=models.ForeignKey(Grouping, null=True, on_delete=models.SET_NULL)


class ParticipantType(models.Model):
    PARTICIPANT='P'
    VOLUNTEER='V'
    STAFF='S'
    TYPE_CHOICES=(
        (PARTICIPANT, 'Participant'),
        (VOLUNTEER, 'Volunteer'),
        (STAFF, 'Staff')
    )

    class Meta:  # Sets up PK as (participant_id, participant_type)
        unique_together=(('participant_id','participant_type'))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    participant_type=models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        primary_key=True
    )


class Diagnosis(models.Model):
    PRIMARY='P'
    SECONDARY='S'
    DIAGNOSIS_CHOICES=(
        (PRIMARY, 'Primary'),
        (SECONDARY, 'Secondary')
    )

    class Meta: # Sets up PK as (participant_id, diagnosis)
        unique_together=(('participant_id','diagnosis'))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    diagnosis=models.CharField(max_length=255, primary_key=True)
    diagnosis_type=models.CharField(
        max_length=1,
        choices=DIAGNOSIS_CHOICES,
    )


class MediaRelease(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(('participant_id','date'))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    consent=models.CharField(max_length=1, choices=YES_NO_CHOICES)
    signature=models.CharField(max_length=NAME_LENGTH)


class BackgroundCheck(models.Model):
    class Meta: # Sets up PK as (participant_id, date)
        unique_together=(('participant_id','date'))

    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE)
    date=models.DateField(primary_key=True)
    signature=models.CharField(max_length=NAME_LENGTH)
    driver_license_num=models.CharField(max_length=18)
