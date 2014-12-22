import os
from django.contrib.auth.models import User

__author__ = 'oguzhan'

from django.db import models


class message(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=1000)
    to_email = models.CharField(max_length=150)
    salt = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(null=True, blank=True, upload_to="attachment/")
    cdate = models.DateTimeField(auto_now_add=True)


