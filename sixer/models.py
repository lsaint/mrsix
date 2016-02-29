
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models


class Experience(models.Model):
    userId = models.CharField(max_length=64, db_index=True)
    ctime = models.DateTimeField(default=now)


class Share2(models.Model):
    user = models.ForeignKey(User)
    rid = models.CharField(max_length=16, db_index=True)
    result = models.PositiveIntegerField(default=1)
    ctime = models.DateTimeField(default=now)
