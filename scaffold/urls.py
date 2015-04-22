from django.conf.urls import patterns, include, url
from django.conf import settings

import session_csrf
session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^blog/', include('blog.urls')),
    url(r'^_ah/', include('djangae.urls')),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),

    url(r'^csp/', include('cspreports.urls')),
)


if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (
            r'^static/(?P<path>.*)$',
             'django.views.static.serve',
            {
                'document_root': settings.STATIC_ROOT
            }
        ),
        (
            r'^media/(?P<path>.*)$',
             'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT
            }
        ),
    )