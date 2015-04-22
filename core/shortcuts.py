import re
import os

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import TemplateDoesNotExist, RequestContext
from django.http import Http404

from .constants import REMOVE_LIST

### Helper functions and shortcuts ###


class NotImplemented(object):

    def __init__(self, obj):
        if not hasattr(obj, "im_class"):
            raise TypeError("Must be class / instance method.")
        self.obj = obj

    def __call__(self, *args, **kwargs):
        msg = "{0} is missing {1}.".format(
            self.obj.im_class.__name__,
            self.obj.__name__
        )
        raise NotImplemented(msg)


def not_implemented(func):
    """Decorator for class methods."""
    def wrapped(*args, **kwargs):
        msg = "{0} is missing {1}.".format(
            args[0].__class__.__name__,
            func.__name__
        )
        raise NotImplementedError(msg)
    return wrapped


def get_or_none(model, **kwargs):
    """ Returns None or model instance
        model -- Django Model name (e.g.: MyModel)
        kwargs -- ORM query arguments (e.g.: title="foo")
    """
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def render_or_404(template_name, dictionary=None, context_instance=None):
    """Helper for testing template existence."""
    try:
        return render_to_response(template_name, dictionary, context_instance)
    except TemplateDoesNotExist:
        raise Http404


def page_loader(request, page='index'):
    """ Helper view for rendering any given template
        URL: /<any_other_page>/
        page -- template name (default - index)
     """
    return render_or_404(page+'.html', RequestContext(request))


def is_array(items):
    return isinstance(items, (list, tuple))


def is_str(obj):
    return isinstance(obj, str)


def is_str_or_u(obj):
    return isinstance(obj, (str, unicode))


def implode(items, glue=''):
    """ Glues array items to string.
        Usage: implode(['a', 'b'], '') -> 'ab'
        items -- array to glue
        glue -- string to use for glue (default - '')
    """
    if is_array(items) and is_str(glue):
        return glue.join(items)
    return -1


def explode(var, sep='', maxsplit=None):
    """ To array on sep
        Usage: explode('abc', '') -> ['a', 'b', 'c']
        var -- string to separate
        sep -- character to split on (default - '')
        maxsplit -- max number of elements to return with split()
    """
    if sep not in var:
        return [var, ]
    if is_str(sep):
        if maxsplit >= 0:
            return var.split(sep, maxsplit)
        elif maxsplit is None:
            return var.split(sep)
        else:
            return var.split(sep)[:maxsplit]
    return -1


def short_slugify(inStr):
    """Slugify a title removing short words."""
    aslug = inStr.lower()
    for a in REMOVE_LIST:
        aslug = re.sub(r'\b'+a+r'\b', ' ', aslug)
    aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
    aslug = re.sub('\s+', '-', aslug)
    return aslug


def key_from_value(dict_to_use, val):
    """Usage - key_from_value({'abc': 1}, 1) -> 'abc'"""
    try:
        return (k for k, v in dict_to_use.items() if v == val).next()
    except StopIteration:
        return -1


def delete_image(path):
    image_path = os.path.join(
        settings.MEDIA_ROOT, str(path)
    )
    try:
        os.remove(image_path)
    except:
        pass