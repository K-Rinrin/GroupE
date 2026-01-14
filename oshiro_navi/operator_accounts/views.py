from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from .forms import AdminUserCreateForm


# Create your views here.
class OperatorTopView(TemplateView):
    template_name = "operator_top.html"

class AdminAccountListView(TemplateView):
    template_name = "admin_account_list.html"

class AdminAccountCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AdminUserCreateForm
    template_name = "admin_account_create.html"
    success_url = reverse_lazy('operator_accounts:account_create_success') # リスト画面へ

    def test_func(self):
        # ログインしているのが「運営（スーパーユーザー）」かチェック
        return self.request.user.is_superuser

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
