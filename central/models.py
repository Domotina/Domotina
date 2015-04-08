from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    filename = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='files/')