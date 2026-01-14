from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class AdminLoginView(TemplateView):
    template_name = "admin_login.html"

class AdminLogoutView(TemplateView):
    template_name = "admin_logout.html"

class AdminTopView(TemplateView):
    template_name = "admin_top.html"

class ContactView(TemplateView):
    template_name = "contact_form.html"

class ContactConfirmView(TemplateView):
    template_name = "contact_confirm.html"

