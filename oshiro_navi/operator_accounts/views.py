from django.shortcuts import render
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from .forms import AdminUserCreateForm
from django.contrib.auth import get_user_model

# Create your views here.
User = get_user_model()

class OperatorTopView(TemplateView):
    template_name = "operator_top.html"

class AdminAccountListView(TemplateView):
    template_name = "admin_account_list.html"

class AdminAccountCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AdminUserCreateForm
    template_name = "admin_account_create.html"
    success_url = reverse_lazy('operator_accounts:account_create_success') 

    def test_func(self):
        # 運営（スーパーユーザー）のみ実行可能
        return self.request.user.is_superuser

class AdminAccountCreateSuccessView(TemplateView):
    template_name = "admin_account_create_success.html"

class AdminAccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = "admin_account_delete.html"
    success_url = reverse_lazy('operator_accounts:account_delete_success')

    def test_func(self):
        # 運営（スーパーユーザー）のみ実行可能
        return self.request.user.is_superuser

class AdminAccountDeleteSuccessView(TemplateView):
    template_name = "admin_account_delete_success.html"

class OperatorLoginView(LoginView):
    template_name = "operator_login.html"

class OperatorLogoutView(TemplateView):
    template_name = "operator_logout.html"
