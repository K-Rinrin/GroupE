from django.shortcuts import render
from django.views.generic import TemplateView

class BasicInfoListView(TemplateView):
    template_name = "basic_info_list.html"

class BasicInfoUpdateView(TemplateView):
    template_name = "basic_info_update.html"

class BasicInfoUpdateSuccessView(TemplateView):
    template_name = "basic_info_update_success.html"

