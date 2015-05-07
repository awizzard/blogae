from django.db import models
from django.core.urlresolvers import reverse

from core.models import Content

from . import managers


class Post(Content):

    previous = models.ForeignKey("Post", blank=True, null=True)
    objects = managers.PostManager()

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug": self.slug})

    @property
    def replies(self):
        return self.post_set.order_by('created')

    @property 
    def original(self):
        return self.previous is None