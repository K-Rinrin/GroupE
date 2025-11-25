from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class UserTopView(TemplateView):
    template_name = "user_top.html"

class UserlogoutView(TemplateView):
    template_name = "user_logout.html"