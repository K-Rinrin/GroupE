from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class OshiroInfoListView(TemplateView):
    template_name = "oshiro_info_list.html"

class OshiroInfoRegisterView(TemplateView):
    template_name = "oshiro_info_register.html"

class OshiroInfoRegisterSuccessView(TemplateView):
    template_name = "oshiro_info_register_success.html"

class OshiroInfoUpdateView(TemplateView):
    template_name = "oshiro_info_update.html"

class OshiroInfoUpdateSuccessView(TemplateView):
    template_name = "oshiro_info_update_success.html"