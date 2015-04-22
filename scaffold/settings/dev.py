from scaffold.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")

