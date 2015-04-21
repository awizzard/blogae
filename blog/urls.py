from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # ex: /blog/
    url(r'^$', views.home, name='home'),
    # ex: /blog/5/
    url(r'^(?P<blog_id>\d+)/$', views.detail, name='detail'),
    # ex: /blog/5/update/
    url(r'^(?P<blog_id>\d+)/update/$', views.update, name='update'),
    # ex: /blog/create/
    url(r'^create/$', views.create, name='create'),
)
