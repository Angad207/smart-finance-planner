from django.db import models
from datetime import datetime, timezone

from django.db.models import OneToOneField
from django.utils import timezone
from django.contrib.auth.models import User
# from django.db import models
# from django.utils import timezone



# Create your models here.

class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    address1= models.CharField(max_length=100)
    address2= models.CharField(max_length=100)
    city= models.CharField(max_length=100)
    state= models.CharField(max_length=100)
    zip = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.fname

class Aamount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    category = models.CharField(max_length=200)
    desc = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.category



class Aincome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    category = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.desc


class Profile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11)

class ADDGOALS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goalname = models.CharField(max_length=110)
    goaltype = models.CharField(max_length=100)
    targetamount = models.FloatField(default=0)
    targetdate = models.DateTimeField(default=timezone.now)
    currentsaving = models.FloatField(default=0)
    prioritystatus = models.CharField(max_length=11, default='off', blank=True)
    aistatus = models.CharField(max_length=11, default='off')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.goalname


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=110)
    budgeted = models.FloatField(default=0)
    spent = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.category




class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

