from django.db import models


class Content(models.Model):
    text = models.CharField(max_length=600)
    created = models.DateTimeField()