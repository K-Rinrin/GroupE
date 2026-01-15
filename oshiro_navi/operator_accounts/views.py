from django.shortcuts import render
from django.views.generic import CreateView, DeleteView,ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from operator_oshiro_info.models import OshiroInfo
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import AdminUserCreateForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.urls import reverse

# Create your views here.
User = get_user_model()

class OperatorTopView(TemplateView):
    template_name = "operator_top.html"

class OperatorContactList(TemplateView):
    template_name = "operator_contact_list.html"

class OperatorContactForm(TemplateView):
    template_name = "operator_contact_form.html"

class OperatorContactConfirm(TemplateView):
    template_name = "operator_contact_confirm.html"

class AdminAccountListView(ListView):
    model = User # get_user_model()したもの
    template_name = 'admin_account_list.html'
    context_object_name = 'account_list'

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'admin_profile',
            'admin_profile__oshiro_management1',
            'admin_profile__oshiro_management2',
            'admin_profile__oshiro_management3',
            'admin_profile__oshiro_management4',
            'admin_profile__oshiro_management5',
        ).filter(is_staff=True)

        # 
        q_word = self.request.GET.get('search')
        if q_word:
            queryset = queryset.filter(
                Q(username__icontains=q_word) | 
                Q(email__icontains=q_word)
            )
        
        return queryset

class AdminAccountCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AdminUserCreateForm
    template_name = "admin_account_create.html"
    success_url = reverse_lazy('operator_accounts:account_create_success') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # HTMLで「castle_list」という名前でお城の全データを使えるようにする
        context['castle_list'] = OshiroInfo.objects.all()
        return context

    def test_func(self):
        # 運営（スーパーユーザー）のみ実行可能
        return self.request.user.is_superuser

class AdminAccountCreateSuccessView(TemplateView):
    template_name = "admin_account_create_success.html"

class AdminAccountDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('operator_accounts:account_delete_success')

    template_name = 'admin_account_list.html' 

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class AdminAccountDeleteSuccessView(TemplateView):
    template_name = "admin_account_delete_success.html"

# ログイン画面
class OperatorLoginView(View):
    def get(self, request):
        # すでにログイン済みならトップへ飛ばす
        if request.user.is_authenticated:
            return redirect('operator_accounts:top')
        return render(request, 'operator_login.html')

    def post(self, request):
        admin_id = request.POST.get('id')
        admin_pass = request.POST.get('pass')

        # 1. ユーザーを認証する（DjangoのUserモデルと照合）
        user = authenticate(request, username=admin_id, password=admin_pass)

        if user is not None:
            # 認証成功した場合
            login(request, user)
            return redirect('operator_accounts:top')
        else:
            # 認証失敗した場合
            context = {
                'error': 'IDまたはパスワードが正しくありません。',
                'prev_id': admin_id,
            }
            return render(request, 'operator_login.html', context)
        

# ログアウト画面
class OperatorLogoutView(LogoutView):
    template_name = "operator_logout.html"
