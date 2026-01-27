from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages # エラーメッセージ用


# Create your views here.
# ログイン後画面
class AdminTopView(LoginRequiredMixin, TemplateView):
    template_name = "admin_top.html"
    login_url = reverse_lazy("admin_accounts:login")

    def dispatch(self, request, *args, **kwargs):
        # ログイン必須（未ログインは login_urlへ）
        response = super().dispatch(request, *args, **kwargs)

        # ✅ ここに来る時点でログイン済み。管理者でなければログインへ返す
        if not hasattr(request.user, "admin_profile"):
            logout(request)
            return redirect("admin_accounts:login")

        return response

# ログアウト画面
class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'admin_logout.html')


# ログイン画面
class AdminLoginView(View):
    def get(self, request):
        # すでにログイン済みで管理者の場合はトップへ
        if request.user.is_authenticated and hasattr(request.user, 'admin_profile'):
            return redirect('admin_accounts:top')
        return render(request, 'admin_login.html')

    def post(self, request):
        admin_id = request.POST.get('id')
        admin_pass = request.POST.get('pass')

        # 1. 認証（IDとパスワードの照合）
        user = authenticate(request, username=admin_id, password=admin_pass)

        if user is not None:
            # 2. 管理者プロフィールを持っているかチェック
            if hasattr(user, 'admin_profile'):
                login(request, user)
                return redirect('admin_accounts:top')
            else:
                # ユーザーは存在するが、管理者ではない場合
                context = {
                    'error': 'このアカウントには管理者権限がありません。',
                    'prev_id': admin_id,
                }
                return render(request, 'admin_login.html', context)
        else:
            # 認証失敗
            context = {
                'error': '管理者IDまたはパスワードが正しくありません。',
                'prev_id': admin_id,
            }
            return render(request, 'admin_login.html', context)




