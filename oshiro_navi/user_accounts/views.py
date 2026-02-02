from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from operator_oshiro_info.models import OshiroInfo
from admin_basic_info.models import BasicInfo
from event_info_management.models import OperatorEvent, AdminEvent
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta



User = get_user_model()


# 1. ログイン後のtop画面
class UserTopView(LoginRequiredMixin,TemplateView):
    template_name = "user_top.html"
    login_url = reverse_lazy("user_accounts:account")
    redirect_field_name = "next"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = timezone.now().date()
        end_of_week = today + timedelta(days=7)
        
        # --- お城リストをランダムに3つだけ取得するように修正 ---
        # order_by('?') でランダムに並び替え、[:3] で先頭の3件を取得します
        context['oshiro_list'] = OshiroInfo.objects.all().select_related('basicinfo').order_by('?')[:3]
        
        # --- 最新イベント情報の取得 ---
        admin_qs = AdminEvent.objects.filter(
            public_settings=True,
            start_date__lte=end_of_week,
            end_date__gte=today
        ).order_by('start_date')

        operator_qs = OperatorEvent.objects.filter(
            public_settings=True,
            start_date__lte=end_of_week,
            end_date__gte=today
        ).order_by('start_date')

        admins = list(admin_qs)
        operators = list(operator_qs)
        for e in admins: e.event_type = 'admin'
        for e in operators: e.event_type = 'operator'

        all_events = sorted(admins + operators, key=lambda x: x.start_date)
        
        context['latest_events'] = all_events
        return context



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
    def get_context_with_bg(self, extra_context=None):
        """背景画像を含めたコンテキストを作成する共通メソッド"""
        # 公開設定のお城からランダムに1つ取得（画像があるものに限定）
        # select_relatedなどは不要なのでシンプルに取得
        random_oshiro = OshiroInfo.objects.exclude(oshiro_images="").order_by('?').first()
        
        context = {
            'bg_image_url': random_oshiro.oshiro_images.url if random_oshiro else None,
            'oshiro_name': random_oshiro.oshiro_name if random_oshiro else ""
        }
        if extra_context:
            context.update(extra_context)
        return context

    def get(self, request):
        # 共通メソッドを使って画像付きでレンダリング
        return render(request, 'user_account.html', self.get_context_with_bg())
    
    
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
                return render(request, 'user_account.html', {
                    'success_message': 'アカウント登録が完了しました。ログインしてください。',
                    'active_form': 'login',
                    'values': {'email': email}  
                })

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