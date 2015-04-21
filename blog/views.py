from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello, world. You're at the blog.")


def detail(request, blog_id):
    return HttpResponse("Hello, world. You're at the blog.")


def update(request, blog_id):
    return HttpResponse("Hello, world. You're at the blog.")


def create(request):
    return HttpResponse("Hello, world. You're at the blog.")