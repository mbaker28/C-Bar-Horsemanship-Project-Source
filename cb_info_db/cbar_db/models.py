from django.db import models

# Constants and Choices
NAME_LENGTH=75
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
PHONE_LENGTH=15

class Participant(models.Model):
    participant_ID=models.AutoField(primary_key=True) # Auto generated PK
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
    participant_id=models.ForeignKey(Participant, on_delete=models.CASCADE) # VERIFY THAT WE WANT CASCADE HERE
    name=models.CharField(max_length=NAME_LENGTH)
    phone=models.CharField(max_length=PHONE_LENGTH)
