from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.utils.crypto import get_random_string

import datetime

now = datetime.datetime.now()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    college = models.CharField(max_length=20, blank=True)
    major = models.CharField(max_length=20, blank=True)
    admission_year = models.IntegerField(validators=[MaxValueValidator(now.year), MinValueValidator(1950)], blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class VerifyToken(models.Model):
    token = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(User, models.CASCADE, related_name='verify_token')

class Club(models.Model):
    name = models.CharField(max_length=20)
    admin = models.ManyToManyField(User, related_name='club_admin')
    members = models.ManyToManyField(User, related_name='club_members')
    waitings = models.ManyToManyField(User, related_name='club_waitings')
    scope = models.CharField(max_length=20)
    category = models.CharField(max_length=20)
    introduction = models.TextField()

class Event(models.Model):
    name = models.CharField(max_length=20)
    content = models.TextField()
    date = models.DateTimeField()
    club = models.ForeignKey(Club, related_name='events', on_delete=models.CASCADE)
    # planning to go / not go (future event)
    future_attendees = models.ManyToManyField(User, related_name='future_attend_events')
    future_absentees = models.ManyToManyField(User, related_name='future_absent_events')
    # have attended (past event)
    past_attendees = models.ManyToManyField(User, related_name='past_attend_events')
