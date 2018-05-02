import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, User
from django.dispatch import receiver
from django.db.models.signals import post_save

from .choices import *

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    patronymic = models.CharField(max_length=30, blank=True, null=True, help_text='Необязательное поле')
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    university = models.CharField(max_length=80, blank=True, null=True)
    degree = models.CharField(choices=DEGREE, default=None, max_length=3, blank=True, null=True)
    educ_start = models.SmallIntegerField(blank=True, null=True)
    educ_end = models.SmallIntegerField(blank=True, null=True)
    programme = models.CharField(max_length=100, blank=True, null=True)
