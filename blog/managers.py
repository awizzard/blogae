from django.db import models
from core.managers import *


class PostQuerySet(ContentQuerySet):

    def originals(self):
        return self.filter(previous__isnull=True)


class PostManager(ContentManager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def originals(self):
        return self.get_queryset().originals()
