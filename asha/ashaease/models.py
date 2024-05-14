from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class ProfileDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    district = models.CharField(max_length=25, null=True)
    asha_id = models.CharField(max_length=25, null=True)
    health_center = models.CharField(max_length=25, null=True)
    mobile_no = models.IntegerField(null=True)
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    blood_grp = models.CharField(max_length=5, null=True)
    aadhar_no = models.IntegerField(null=True)
    address = models.CharField(max_length=50, null=True)
    office_address = models.CharField(max_length=50, null=True)
    is_updated = models.BooleanField(default=False)

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=100)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.title} on {self.event_date} from {self.start_time} to {self.end_time}"
    

class Report(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")

    def __str__(self):
        return self.name

class Heading(models.Model):
    report = models.ForeignKey(Report, related_name='headings', on_delete=models.CASCADE)
    heading = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.heading
    
class Questions(models.Model):
    heading = models.ForeignKey(Heading, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=1000)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text
    

class House(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="houses")
    house_no = models.CharField(max_length=20)
    house_address = models.TextField()
    no_of_members = models.IntegerField(default=0)
    added_no_of_members = models.IntegerField(default=0)
    is_no_of_members_added = models.BooleanField(default=False)
    child_onboard = models.BooleanField(default=False)
    child_cound = models.IntegerField(default=0)
    added_child_cound = models.IntegerField(default=0)
    is_child_added = models.BooleanField(default=False)
    pregnant_onboard = models.BooleanField(default=False)
    pregnant_cound = models.IntegerField(default=0)
    added_pregnant_cound = models.IntegerField(default=0)
    is_pregnant_added = models.BooleanField(default=False)
    patients_onboard = models.BooleanField(default=False)
    patients_cound = models.IntegerField(default=0)
    added_patients_cound = models.IntegerField(default=0)
    is_patients_added = models.BooleanField(default=False)

class Members(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    dob = models.DateField()
    age = models.IntegerField(default=0)
    qualification = models.CharField(max_length=30)
    occupation = models.CharField(max_length=30)
    habit = models.BooleanField(default=False)
    habittype = models.CharField(max_length=20, null=True)

class Children(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    delivery = models.BooleanField(default=False)
    threemonth = models.BooleanField(default=False)
    sixmonth = models.BooleanField(default=False)
    oneyear = models.BooleanField(default=False)
    fiveyear = models.BooleanField(default=False)
    tenyear = models.BooleanField(default=False)
    fifteenyear = models.BooleanField(default=False)
    reason = models.TextField()

class Pregnant(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    pregnancy_months = models.IntegerField(default=0)
    month1_weight = models.BooleanField(default=False)
    month1_bp = models.BooleanField(default=False)
    month1_hr = models.BooleanField(default=False)
    month2_weight = models.BooleanField(default=False)
    month2_bp = models.BooleanField(default=False)
    month2_hr = models.BooleanField(default=False)
    month3_weight = models.BooleanField(default=False)
    month3_bp = models.BooleanField(default=False)
    month3_hr = models.BooleanField(default=False)
    month4_weight = models.BooleanField(default=False)
    month4_bp = models.BooleanField(default=False)
    month4_hr = models.BooleanField(default=False)
    month5_weight = models.BooleanField(default=False)
    month5_bp = models.BooleanField(default=False)
    month5_hr = models.BooleanField(default=False)
    month6_weight = models.BooleanField(default=False)
    month6_bp = models.BooleanField(default=False)
    month6_hr = models.BooleanField(default=False)
    month7_weight = models.BooleanField(default=False)
    month7_bp = models.BooleanField(default=False)
    month7_hr = models.BooleanField(default=False)
    month8_weight = models.BooleanField(default=False)
    month8_bp = models.BooleanField(default=False)
    month8_hr = models.BooleanField(default=False)
    month9_weight = models.BooleanField(default=False)
    month9_bp = models.BooleanField(default=False)
    month9_hr = models.BooleanField(default=False)
    month10_weight = models.BooleanField(default=False)
    month10_bp = models.BooleanField(default=False)
    month10_hr = models.BooleanField(default=False)


class Patient(models.Model):
    member = models.ForeignKey(Members, on_delete=models.CASCADE)
    disease_details = models.TextField()
    pain = models.BooleanField(default=False)
    disease = models.BooleanField(default=False)