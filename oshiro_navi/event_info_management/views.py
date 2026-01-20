from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django import forms
from operator_accounts.models import Operator
from admin_accounts.models import Admin
from .models import OperatorEvent,AdminEvent
from django.db.models import Q
from django.views.generic import TemplateView

# Create your views here.
# class OperatorTopView(TemplateView):
#     template_name = "operator_top.html"

class AdminEventInfoListView(ListView):
    model = AdminEvent
    template_name = "admin_event_info_list.html"
    context_object_name = 'admin_events'

    def get_queryset(self):
        if hasattr(self.request.user, 'admin_profile'):
            return AdminEvent.objects.filter(admin=self.request.user.admin_profile).order_by('-start_date')
        return AdminEvent.objects.none()

class AdminEventInfoRegisterView(CreateView):
    model = AdminEvent
    template_name = "admin_event_info_register.html"
    fields = ['event_info', 'event_overview', 'venue', 'start_date', 'end_date', 'start_time', 'end_time', 'public_settings']
    success_url = reverse_lazy('event_info_management:admin_event_info_register_success')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        admin_profile = self.request.user.admin_profile

        # 担当しているお城1〜5の中から、データが入っているものだけをリスト化
        managed_castles = []
        slots = [
            admin_profile.oshiro_management1,
            admin_profile.oshiro_management2,
            admin_profile.oshiro_management3,
            admin_profile.oshiro_management4,
            admin_profile.oshiro_management5,
        ]
        
        # Noneでないお城を（ID, 名前）のタプル形式で追加
        choices = [(castle.oshiro_name, castle.oshiro_name) for castle in slots if castle]
        
        # venue（開催場所）の入力欄を、テキスト自由入力から「選択式（Select）」に変更
        form.fields['venue'] = forms.ChoiceField(choices=choices, label="開催場所（担当お城）")
        
        return form

    def form_valid(self, form):
        if hasattr(self.request.user, 'admin_profile'):
            # 【修正】 author → admin に変更
            form.instance.admin = self.request.user.admin_profile
            return super().form_valid(form)
        else:
            raise PermissionDenied("管理者プロフィールがありません")

class AdminEventInfoRegisterSuccessView(TemplateView):
    template_name = "admin_event_info_register_success.html"
    
class AdminEventInfoUpdateView(UpdateView):
    model = AdminEvent
    template_name = "admin_event_info_update.html"
    fields = ['event_info', 'event_overview', 'venue', 'start_date', 'end_date', 'start_time', 'end_time', 'public_settings']
    
    def get_success_url(self):
        # 更新成功時の遷移先
        return reverse_lazy('event_info_management:admin_event_info_update_success')

    def get_queryset(self):
        # 自分が登録したイベントのみ編集可能にする
        return AdminEvent.objects.filter(admin=self.request.user.admin_profile)

    def get_form(self, form_class=None):
        """
        登録時と同じように、venue（開催場所）を
        担当お城のプルダウンに変更する処理
        """
        form = super().get_form(form_class)
        admin_profile = self.request.user.admin_profile

        # 担当しているお城1〜5をリスト化
        slots = [
            admin_profile.oshiro_management1,
            admin_profile.oshiro_management2,
            admin_profile.oshiro_management3,
            admin_profile.oshiro_management4,
            admin_profile.oshiro_management5,
        ]
        
        # 登録されているお城のみをプルダウンの選択肢にする
        choices = [(castle.oshiro_name, castle.oshiro_name) for castle in slots if castle]
        
        # フォームのvenueフィールドをプルダウンに書き換え
        form.fields['venue'] = forms.ChoiceField(choices=choices, label="開催場所（担当お城）")
        
        return form

class AdminEventInfoUpdateSuccessView(TemplateView):
    template_name = "admin_event_info_update_success.html"

class AdminEventInfoDeleteView(LoginRequiredMixin, DeleteView):
    model = AdminEvent
    template_name = "admin_event_info_delete.html"
    
    def get_success_url(self):
        # 削除成功後の遷移先
        return reverse_lazy('event_info_management:admin_event_info_delete_success')

    def get_queryset(self):
        # 自分が登録したイベントのみ削除可能にする（セキュリティ対策）
        return AdminEvent.objects.filter(admin=self.request.user.admin_profile)


class AdminEventInfoDeleteSuccessView(TemplateView):
    template_name = "admin_event_info_delete_success.html"

class AdminEventInfoDetailView(DetailView):
    model = AdminEvent
    template_name = "admin_event_info_detail.html"
    context_object_name = 'event' # テンプレートで使う変数名

    def get_queryset(self):
        # セキュリティ：自分が登録したイベントのみ閲覧可能にする
        return AdminEvent.objects.filter(admin=self.request.user.admin_profile)

# ここからoperator

class OperatorEventInfoListView(ListView):
    model = OperatorEvent
    template_name = "operator_event_info_list.html"
    context_object_name = 'event_list'

    def get_queryset(self):
        # ログインユーザーに紐づくOperatorを直接取得しにいく
        operator_profile = Operator.objects.filter(account=self.request.user).first()
        
        if operator_profile:
            # プロフィールが見つかった場合
            queryset = OperatorEvent.objects.filter(operator=operator_profile)
        # else:
        #     # 見つからない場合は全件表示（デバッグ用：これで表示されるなら判定ミス確定）
        #     print(f"DEBUG: User {self.request.user} has no Operator profile.")
        #     return OperatorEvent.objects.all() 

        # 検索機能
        q_word = self.request.GET.get('search')
        if q_word:
            queryset = queryset.filter(
                Q(event_info__icontains=q_word) | 
                Q(venue__icontains=q_word)
            )
        
        return queryset.order_by('-start_date')

class OperatorEventInfoRegisterView(CreateView):
    model = OperatorEvent
    template_name = "operator_event_info_register.html"
    fields = ['event_info', 'event_overview', 'venue', 'start_date', 'end_date', 'start_time', 'end_time', 'public_settings']
    success_url = reverse_lazy('event_info_management:operator_event_info_register_success')

    def form_valid(self, form):
        # 1. ログインユーザーに紐づくOperatorプロフィールを取得
        # (先ほど調べた通り、フィールド名は account)
        operator_profile = Operator.objects.get(account=self.request.user)
        
        # 2. 保存する前にoperatorをセット
        form.instance.operator = operator_profile
        
        return super().form_valid(form)

class OperatorEventInfoRegisterSuccessView(TemplateView):
    template_name = "operator_event_info_register_success.html"
    
class OperatorEventInfoUpdateView(UpdateView):
    model = OperatorEvent
    template_name = "operator_event_info_update.html"
    fields = ['event_info', 'event_overview', 'venue', 'start_date', 'end_date', 'start_time', 'end_time', 'public_settings']
    
    def get_success_url(self):
        return reverse_lazy('event_info_management:operator_event_info_update_success')

    def get_queryset(self):
        # ログイン中のオペレーターに紐づくイベントのみに限定（他人のイベントをURL直打ちで編集させないため）
        operator_profile = Operator.objects.get(account=self.request.user)
        return OperatorEvent.objects.filter(operator=operator_profile)

class OperatorEventInfoUpdateSuccessView(TemplateView):
    template_name = "operator_event_info_update_success.html"

class OperatorEventInfoDeleteView(DeleteView):
    model = OperatorEvent
    template_name = "operator_event_info_delete.html" # 確認画面
    success_url = reverse_lazy('event_info_management:operator_event_info_delete_success')

    def get_queryset(self):
        # ログイン中のオペレーターのイベントのみに対象を限定
        operator_profile = Operator.objects.get(account=self.request.user)
        return OperatorEvent.objects.filter(operator=operator_profile)


class OperatorEventInfoDeleteSuccessView(TemplateView):
    template_name = "operator_event_info_delete_success.html"

class OperatorEventInfoDetailView(DetailView):
    model = OperatorEvent
    template_name = "operator_event_info_detail.html"
    context_object_name = 'event' # テンプレートで使う変数名

    def get_queryset(self):
        # セキュリティ：自分のオペレーターに紐づくイベントのみ閲覧可能にする
        operator_profile = Operator.objects.get(account=self.request.user)
        return OperatorEvent.objects.filter(operator=operator_profile)