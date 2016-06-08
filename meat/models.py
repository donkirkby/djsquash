from __future__ import unicode_literals

from django.db import models


class Bacon(models.Model):
    name = models.CharField(max_length=30)
    apple = models.ForeignKey('fruit.Apple')
