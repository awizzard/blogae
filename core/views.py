import json
import operator

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.db.models import Q

from .shortcuts import not_implemented, is_array


class NotFoundMixin(object):

    not_found_msg = "Nothing found for you!"

    def get_object(self, queryset=None):
        obj = super(NotFoundMixin, self).get_object(queryset)
        if not obj:
            messages.error(self.request, self.not_found_msg)
        return obj


class ContextVariableMixin(object):
    """
    Mixin for setting context data using class attributes.
    Example:
        class MyClass(ContextVariableMixin):
            prefix = "context_"
            context_bar = "foo"
        MyClass().get_context_data()["bar"] => "foo"
    """

    prefix = "context_"

    def get_context_data(self, **kwargs):
        context = super(
            ContextVariableMixin,
            self
        ).get_context_data(**kwargs)
        context.update(
            {
                var[len(self.prefix):]: getattr(self, var)
                for var in dir(self)
                if var.startswith(self.prefix)
            }
        )
        return context


class TitleContextMixin(object):

    def __get_title(self):
        if hasattr(self, "model"):
            return self.model._meta.verbose_name_plural.title()
        return ''

    def get_context_data(self, **kwargs):
        context = super(
            TitleContextMixin,
            self
        ).get_context_data(**kwargs)
        context.update(
            {
                "title": self.__get_title()
            }
        )
        return context


class ActionMixin(object):

    @property
    @not_implemented
    def action(self):
        pass

    @property
    @not_implemented
    def model_label(self):
        pass

    def form_valid(self, form):
        msg = "{0} {1}!".format(self.model_label.title(), self.action)
        messages.success(self.request, msg)
        return super(ActionMixin, self).form_valid(form)


class RandomObjectMixin(object):

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.order_by('?')[0]
        except (ObjectDoesNotExist, IndexError):
            return queryset.none()
        return obj


class ActiveMixin(object):

    def get_queryset(self):
        queryset = super(ActiveMixin, self).get_queryset()
        return queryset.are_active()


class AuthoredMixin(object):

    def form_valid(self, form):
        if hasattr(form, "instance"):
            form.instance.author = self.request.user
        return super(AuthoredMixin, self).form_valid(form)


class LatestMixin(object):

    def get_object(self, queryset=None):
        return self.model.objects.latest()