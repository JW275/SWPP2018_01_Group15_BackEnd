from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

now = datetime.datetime.now()

class User(AbstractUser):
    name = models.CharField(max_length=20)
    college = models.CharField(max_length=20)
    major = models.CharField(max_length=20)
    admission_year = models.IntegerField(validators=[MaxValueValidator(now.year), MinValueValidator(1950)]) 
