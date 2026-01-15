from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()


# 1. ログイン後の画面
class UserTopView(TemplateView):
    template_name = "user_top.html"



# 2.   ログアウト処理
# 2-1. ログアウト確認画面
class UserlogoutCheckView(TemplateView):
    template_name = "user_logout_check.html"

#2-2. ログアウト画面
class UserlogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'user_logout.html')


# 3. アカウント処理（ログイン画面表示・登録・ログイン処理）
class UserAccountView(View):
    
    def get(self, request):
        return render(request, 'user_account.html')

    def post(self, request):
        action_type = request.POST.get('action')
        errors = {}
        values = request.POST

        # === 新規登録 (Signup) ===
        if action_type == 'signup':
            username = request.POST.get('username', '').strip()
            email    = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()

            # 2-1. アカウント名未入力
            if not username:
                errors['signup_username'] = 'アカウント名が入力されていません'
            
            # 2-2. Email未入力
            if not email:
                errors['signup_email'] = 'Emailが入力されていません'
        
            # 2-3. Pass未入力
            if not password:
                errors['signup_password'] = 'Passが入力されていません'

            # 2-4. Email重複
            if email and not errors.get('signup_email'):
                if User.objects.filter(email=email).exists():
                    errors['signup_email'] = 'このEmailは既に使用されています'

            # エラーがある場合は画面を再表示
            if errors:
                return render(request, 'user_account.html', {
                    'errors': errors,
                    'values': values,
                    'active_form': 'signup' # JSでパネルを開きっぱなしにする用
                })


            # 登録処理
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return redirect('user_accounts:top') 
            except Exception:
                errors['signup_common'] = '登録処理に失敗しました'
                return render(request, 'user_account.html', {
                    'errors': errors,
                    'values': values,
                    'active_form': 'signup'
                })


        # === ログイン (Login) ===
        elif action_type == 'login':
            email    = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()

            # 2-1. Email未入力
            if not email:
                errors['login_email'] = 'Emailが入力されていません'

            # 2-2. Pass未入力
            if not password:
                errors['login_password'] = 'Passが入力されていません'

            if errors:
                return render(request, 'user_account.html', {
                    'errors': errors,
                    'values': values,
                    'active_form': 'login'
                })

            # 2-3. 認証チェック
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
                # 認証失敗エラー
                errors['login_common'] = 'EmailまたはPassが間違っています'
                return render(request, 'user_account.html', {
                    'errors': errors,
                    'values': values,
                    'active_form': 'login'
                })
        

        return redirect('user_accounts:account')