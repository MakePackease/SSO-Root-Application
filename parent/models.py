from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    users = models.OneToOneField(User, related_name="users", on_delete=models.CASCADE)

    school_name = models.CharField(max_length=10)
    brand = models.CharField(max_length=10)
    classs = models.CharField(max_length=2)
    section = models.CharField(max_length=3)
    enrollment_no = models.CharField(max_length=20)
