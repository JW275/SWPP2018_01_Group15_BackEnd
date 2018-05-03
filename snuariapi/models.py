from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    name = models.CharField(max_length=20)
    admin = models.ManyToManyField(User, related_name='club_admin')
    members = models.ManyToManyField(User, related_name='club_members')
    waitings = models.ManyToManyField(User, related_name='club_waitings')
    scope = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    introduction = models.TextField()
    

