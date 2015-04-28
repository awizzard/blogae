from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.conf import settings 
from django.contrib.messages.views import SuccessMessageMixin

from vanilla import ListView, DetailView, CreateView, UpdateView, RedirectView, TemplateView
from braces.views import LoginRequiredMixin
from termsearch.views import TermSearchMixin

from core import views as core_views

from . import models
from . import forms

from google.appengine.api import users


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
    
    @property 
    def context_logout_url(self):
        return users.create_logout_url(reverse('home'))
    
    @property 
    def context_login_url(self):
        return users.create_login_url(reverse('home'))

    @property
    def context_guser(self):
        return users.get_current_user()
    
    @property 
    def context_head(self):
        q = self.request.GET.get("q")
        if q:
            return "Posts containing `{q}`".format(q=q)
        else:
            return "All Posts"

    @property 
    def context_posts(self):
        return self.get_queryset().exists()

    def get_queryset(self):
        qs = super(PostListView, self).get_queryset()
        if self.request.user.is_staff:
            return qs
        else:
            return qs.are_active()


class PostDetailView(DetailView):

    model = models.Post
    lookup_field = "slug"

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
    SuccessMessageMixin,
    core_views.ContextVariableMixin,
    core_views.AuthoredMixin, 
    CreateView
):

    model = models.Post
    success_message = "Post created!"
    context_title = "New Post"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_form_class(self):
        return forms.PostForm

    def form_valid(self, form):
        return super(PostCreateView, self).form_valid(form)

    def get_login_url(self):
        return users.create_login_url(reverse('new'))


class PostUpdateView(
    LoginRequiredMixin,
    SuccessMessageMixin,  
    core_views.ContextVariableMixin,
    UpdateView
):

    model = models.Post
    lookup_field = "slug"
    form_class = forms.PostForm
    success_message = "Post updated!"
    context_title = "Edit Post"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_login_url(self):
        return users.create_login_url(
            reverse(
                'edit', 
                kwargs={'slug': self.kwargs['slug']}
            )
        )


class AuthoredView(PostListView):

    term_mapping = {
        "title": "icontains",
    }

    @property 
    def context_head(self):
        return "Posts by {}".format(self.kwargs['author'])

    @property
    def context_lead(self):
        q = self.request.GET.get("q")
        return "Posts created by {}{}.".format(
            self.kwargs['author'],
            " matching `{}`".format(q) if q else '' 
        )

    def get_queryset(self):
        qs = super(AuthoredView, self).get_queryset()
        from django.db.models import get_model
        author = get_object_or_404(
            get_model(settings.AUTH_USER_MODEL), 
            email=self.kwargs['author']
        )
        return qs.filter(author=author)


class PostHideView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(models.Post, slug=self.kwargs['slug'])
        post.active = False
        post.save()
        return post.get_absolute_url()


class PostRevealView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(models.Post, slug=self.kwargs['slug'])
        post.active = True
        post.save()
        return post.get_absolute_url()


class PostLatestView(RedirectView):

    permanent = False
    model = models.Post

    def get_redirect_url(self, *args, **kwargs):
        try:
            if self.request.user.is_staff:
                post = self.model.objects.latest()
            else:
                post = self.model.objects.are_active().latest()
        except self.model.DoesNotExist:
            return reverse('home')
        else:        
            return post.get_absolute_url()
