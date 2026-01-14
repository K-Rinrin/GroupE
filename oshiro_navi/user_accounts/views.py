from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages


User = get_user_model()


# 1. ログイン後の画面
class UserTopView(TemplateView):
    template_name = "user_top.html"


# 2. ログアウト処理
class UserlogoutView(View):
    def get(self, request):
        logout(request)
        # ログアウト完了画面を表示する
        return render(request, 'user_logout.html')


# 3. アカウント処理（ログイン画面表示・登録・ログイン処理）
class UserAccountView(View):
    
    # GETリクエスト: ログイン/登録画面
    def get(self, request):
        return render(request, 'user_account.html')

    # POSTリクエスト: 登録またはログイン処理
    def post(self, request):
        action_type = request.POST.get('action')

        # === 新規登録 (Signup) ===
        if action_type == 'signup':
            username = request.POST.get('username')
            email    = request.POST.get('email')
            password = request.POST.get('password')

            # 重複チェック
            if User.objects.filter(email=email).exists():
                messages.error(request, "このメールアドレスは既に登録されています。")
                return redirect('user_accounts:account')
            
            if hasattr(User, 'username'): 
                if User.objects.filter(username=username).exists():
                    messages.error(request, "このアカウント名は既に使用されています。")
                    return redirect('user_accounts:account')

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                
                
                login(request, user)
                return redirect('user_accounts:top') 

            except Exception as e:
                messages.error(request, f"登録エラー: {e}")
                return redirect('user_accounts:account')


        # === ログイン (Login) ===
        elif action_type == 'login':
            email    = request.POST.get('email')
            password = request.POST.get('password')

            user = None
            
            
            try:
                user_obj = User.objects.get(email=email)
                username_field = User.USERNAME_FIELD 
                username_val = getattr(user_obj, username_field)
                
                user = authenticate(request, username=username_val, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                return redirect('user_accounts:top')
            else:
                messages.error(request, "メールアドレスまたはパスワードが間違っています。")
                return redirect('user_accounts:account')


        
        return redirect('user_accounts:account')