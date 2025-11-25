from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
# class OperatorTopView(TemplateView):
#     template_name = "operator_top.html"

class EventInfoListView(TemplateView):
    template_name = "event_info_list.html"

class EventInfoRegisterView(TemplateView):
    template_name = "event_info_register.html"

class EventInfoRegisterSuccessView(TemplateView):
    template_name = "event_info_register_success.html"
    
class EventInfoUpdateView(TemplateView):
    template_name = "event_info_update.html"

class EventInfoUpdateSuccessView(TemplateView):
    template_name = "event_info_update_success.html"

class EventInfoDeleteView(TemplateView):
    template_name = "event_info_delete.html"

class EventInfoDeleteCheckView(TemplateView):
    template_name = "event_info_delete_check.html"

class EventInfoDeleteSuccessView(TemplateView):
    template_name = "event_info_delete_success.html"