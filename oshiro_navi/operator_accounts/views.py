from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class OperatorTopView(TemplateView):
    template_name = "operator_top.html"

class AdminAccountListView(TemplateView):
    template_name = "admin_account_list.html"

class AdminAccountCreateView(TemplateView):
    template_name = "admin_account_create.html"

class AdminAccountCreateSuccessView(TemplateView):
    template_name = "admin_account_create_success.html"

class AdminAccountDeleteView(TemplateView):
    template_name = "admin_account_delete.html"

class AdminAccountDeleteSuccessView(TemplateView):
    template_name = "admin_account_delete_success.html"

class OperatorLoginView(TemplateView):
    template_name = "operator_login.html"

class OperatorLogoutView(TemplateView):
    template_name = "operator_logout.html"
