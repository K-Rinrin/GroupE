from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages # エラーメッセージ用


# Create your views here.
# ログイン後画面
class AdminTopView(TemplateView):
    template_name = "admin_top.html"

# ログアウト画面
class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'admin_logout.html')


# ログイン画面
class AdminLoginView(View):
    def get(self, request):
        # すでにログインしている場合はトップへ
        if request.user.is_authenticated:
            return redirect('admin_accounts:top')
        return render(request, 'admin_login.html')

    def post(self, request):
        admin_id = request.POST.get('id')
        admin_pass = request.POST.get('pass')

        # ユーザー認証
        user = authenticate(request, username=admin_id, password=admin_pass)

        if user is not None:
            # 認証成功した場合
            login(request, user)
            return redirect('admin_accounts:top') # ログイン後TOP画面へ
        else:
            # 認証失敗した場合
            messages.error(request, 'IDまたはパスワードが正しくありません。')
            return render(request, 'admin_login.html')





class ContactView(TemplateView):
    template_name = "admin_contact_form.html"

class ContactConfirmView(TemplateView):
    template_name = "admin_contact_confirm.html"

