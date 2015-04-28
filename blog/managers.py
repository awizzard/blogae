from django.db import models
from core.managers import *


class PostQuerySet(ContentQuerySet):
    pass


class PostManager(ContentManager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)