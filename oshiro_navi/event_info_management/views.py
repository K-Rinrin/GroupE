from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import OperatorEvent,AdminEvent
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

class OperatorEventInfoListView(ListView):
    model = OperatorEvent
    template_name = "operator_event_info_list.html"
    context_object_name = 'event_list'

    ordering = ['-start_date']

class OperatorEventInfoRegisterView(CreateView):
    model = OperatorEvent
    template_name = "operator_event_info_register.html"
    fields = ['event_info', 'event_overview', 'venue', 'start_date', 'end_date', 'start_time', 'end_time', 'public_settings']
    success_url = reverse_lazy('event_info_management:operator_event_info_register_success')

    def form_valid(self, form):
        # ログインしているオペレーターを自動で保存する場合
        # form.instance.operoter = self.request.user.operator_profile
        return super().form_valid(form)

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