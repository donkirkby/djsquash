from __future__ import unicode_literals

from django.db import models


class Apple(models.Model):
    name = models.CharField(max_length=30)
    size = models.IntegerField(default=3)


class Cranberry(models.Model):
    name = models.CharField(max_length=30)
    # TODO: switch back to the foreign key.
    # bacon = models.ForeignKey('meat.Bacon', null=True)
    bacon = models.IntegerField(db_column='bacon_id', null=True)
