from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
# class OperatorTopView(TemplateView):
#     template_name = "operator_top.html"

class AdminEventInfoListView(TemplateView):
    template_name = "admin_event_info_list.html"

class AdminEventInfoRegisterView(TemplateView):
    template_name = "admin_event_info_register.html"

class AdminEventInfoRegisterSuccessView(TemplateView):
    template_name = "admin_event_info_register_success.html"
    
class AdminEventInfoUpdateView(TemplateView):
    template_name = "admin_event_info_update.html"

class AdminEventInfoUpdateSuccessView(TemplateView):
    template_name = "admin_event_info_update_success.html"

class AdminEventInfoDeleteView(TemplateView):
    template_name = "admin_event_info_delete.html"

class AdminEventInfoDeleteCheckView(TemplateView):
    template_name = "admin_event_info_delete_check.html"

class AdminEventInfoDeleteSuccessView(TemplateView):
    template_name = "admin_event_info_delete_success.html"


# ここからoperator

class OperatorEventInfoListView(TemplateView):
    template_name = "operator_event_info_list.html"

class OperatorEventInfoRegisterView(TemplateView):
    template_name = "operator_event_info_register.html"

class OperatorEventInfoRegisterSuccessView(TemplateView):
    template_name = "operator_event_info_register_success.html"
    
class OperatorEventInfoUpdateView(TemplateView):
    template_name = "operator_event_info_update.html"

class OperatorEventInfoUpdateSuccessView(TemplateView):
    template_name = "operator_event_info_update_success.html"

class OperatorEventInfoDeleteView(TemplateView):
    template_name = "operator_event_info_delete.html"

class OperatorEventInfoDeleteCheckView(TemplateView):
    template_name = "operator_event_info_delete_check.html"

class OperatorEventInfoDeleteSuccessView(TemplateView):
    template_name = "operator_event_info_delete_success.html"