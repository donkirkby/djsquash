from __future__ import unicode_literals

from django.db import models


class Apple(models.Model):
    name = models.CharField(max_length=30)
    size = models.IntegerField(default=3)


class Cranberry(models.Model):
    name = models.CharField(max_length=30)
    bacon = models.ForeignKey('meat.Bacon', null=True)
    size = models.IntegerField(default=1)
