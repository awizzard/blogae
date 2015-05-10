from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=views.PostListView.as_view(),
        name="home",
    ),
    url(
        regex=r'^latest/$',
        view=views.PostLatestView.as_view(),
        name="latest",
    ),
    url(
        regex=r'^new/$',
        view=views.PostCreateView.as_view(),
        name="new",
    ),
    url(
        regex=r'^random/$',
        view=views.PostRandomView.as_view(),
        name="random",
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
        view=views.PostRevealView.as_view(),
        name="reveal",
    ),
    url(
        regex=r'^(?P<reply>[\w-]+)/reply/$',
        view=views.PostReplyView.as_view(),
        name="reply",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/root/$',
        view=views.PostRootView.as_view(),
        name="root",
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=views.PostDetailView.as_view(),
        name="post",
    ),

)