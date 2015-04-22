from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=views.PostListView.as_view(),
        name="home",
    ),
    url(
        regex=r'^new/$',
        view=views.PostCreateView.as_view(),
        name="new_post",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/edit/$',
        view=views.PostUpdateView.as_view(),
        name="edit",
    ),
    url(
        regex=r'^by/(?P<author>[^/\\]+)/$',
        view=views.AuthoredView.as_view(),
        name="author",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/hide/$',
        view=views.PostHideView.as_view(),
        name="hide",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/reveal/$',
        view=views.PostHideView.as_view(),
        name="reveal",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=views.PostDetailView.as_view(),
        name="post",
    ),
)