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