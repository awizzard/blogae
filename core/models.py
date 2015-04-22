from django.db import models
from django.conf import settings

from .shortcuts import short_slugify, not_implemented
from .managers import ContentManager
from .constants import *


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-
    updating ''created'' and ''modified'' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Content(TimeStampedModel):
    """
    An abstract base class model for all content that may
    be published on the site.
    """
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name='authored_%(class)ss'
    )
    slug = models.CharField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
        help_text="""
        This is the URL safe name to be used in the URL.
        """,
        blank=True,
        null=True
    )
    active = models.BooleanField(
        "Active/visible content?",
        editable=True,
        default=True
    )
    content = models.TextField(blank=True)
    objects = ContentManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = short_slugify(self.title)
        super(Content, self).save(*args, **kwargs)

    class Meta(TimeStampedModel.Meta):
        abstract = True
        ordering = ['-created']
        get_latest_by = "created"

