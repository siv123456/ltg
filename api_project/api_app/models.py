from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.fname