from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
# class OperatorTopView(TemplateView):
#     template_name = "operator_top.html"

class EventInfoManagementView(TemplateView):
    template_name = "event_info_management.html"