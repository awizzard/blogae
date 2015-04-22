from django.db import models
from django.conf import settings

from .shortcuts import short_slugify, delete_image, not_implemented
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


class Link(TimeStampedModel):
    """
    Abstract class for hosted external URLs.
    """
    title = models.CharField(max_length=MAX_TITLE_LENGTH)
    url = models.URLField()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.title


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


class ImageSwappingModel(models.Model):
    """
    An abstract base class model for handling
    the deletion of old image data on replcement.
    """

    # override with suitable image handling field
    @not_implemented
    def image(self):
        pass

    __original_image = None


    def __init__(self, *args, **kwargs):
        super(ImageSwappingModel, self).__init__(*args, **kwargs)
        self.__original_image = self.image

    def save(self, *args, **kwargs):

        # delete image file if image has changed
        if (
            self.image != self.__original_image
        ) and (
            self.__original_image != ''
        ):
            delete_image(self.__original_image)

        super(ImageSwappingModel, self).save(*args, **kwargs)

        # update original image with new path
        self.__original_image = self.image

    class Meta:
        abstract = True