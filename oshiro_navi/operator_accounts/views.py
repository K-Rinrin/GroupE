from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class OperatorTopView(TemplateView):
    template_name = "operator_top.html"

class AdminAccountListView(TemplateView):
    template_name = "admin_account_list.html"