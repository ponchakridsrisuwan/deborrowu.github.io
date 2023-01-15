from django.db import models
from django.contrib.auth.models import User
from myapp.models import *
from myappstaff.models import *
from myappSuper.models import *
from django.contrib.auth.models import Group
from allauth.socialaccount.models import SocialAccount


class EmailUser(models.Model):
    emailuser = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.emailuser    