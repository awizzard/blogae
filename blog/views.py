from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings 

from vanilla import ListView, DetailView, CreateView, UpdateView, RedirectView, TemplateView
from braces.views import LoginRequiredMixin
from termsearch.views import TermSearchMixin

from core import views as core_views

from . import models
from . import forms


class PostListView(
    core_views.ContextVariableMixin,
    TermSearchMixin,
    ListView
):

    model = models.Post
    term_mapping = {
        "title": "icontains",
    }
    context_head = "All Posts"
    context_lead = "Some posts will be found below. Eventually."


class PostDetailView(DetailView):

    model = models.Post
    lookup_field = "slug"

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        return context

    def get_object(self):
        queryset = self.get_queryset()
        slug = self.kwargs[self.lookup_field]
        if self.request.user.is_authenticated():
            if self.request.user.is_staff:
                return get_object_or_404(
                    queryset,
                    slug=slug
                )
        return get_object_or_404(
            queryset,
            slug=slug,
            active=True
        )


class PostCreateView(
    LoginRequiredMixin, 
    core_views.AuthoredMixin, 
    CreateView
):

    model = models.Post

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_form_class(self):
        return forms.PostForm

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['title'] = "New Post"
        return context

    def form_valid(self, form):
        return super(PostCreateView, self).form_valid(form)


class PostUpdateView(
    LoginRequiredMixin, 
    UpdateView
):

    model = models.Post
    lookup_field = "slug"
    form_class = forms.PostForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Edit Post"
        return context


class AuthoredView(PostListView):

    def get_context_data(self, **kwargs):
        context = super(AuthoredView, self).get_context_data(**kwargs)
        context['head'] = "Posts by {}".format(self.kwargs['author'])
        context['lead'] = "All posts created by {}.".format(
            self.kwargs['author']
        )
        return context

    def get_queryset(self):
        from django.db.models import get_model
        author = get_object_or_404(
            get_model(settings.AUTH_USER_MODEL), 
            email=self.kwargs['author']
        )
        return self.model.objects.filter(author=author)


class PostHideView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(models.Post, slug=self.kwargs['slug'])
        post.active = False
        post.save()
        return post.get_absolute_url()