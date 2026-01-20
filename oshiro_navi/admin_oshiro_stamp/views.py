from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.http import Http404
from admin_accounts.models import Admin

from .models import OshiroStampInfo
from operator_oshiro_info.models import OshiroInfo  # お城情報の参照用
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class AdminOshiroRequiredMixin:
    """ログイン中の管理者が、URLのoshiro_idを担当しているかチェックする"""
    def dispatch(self, request, *args, **kwargs):
        admin = get_object_or_404(Admin, account=request.user)
        oshiro_id = kwargs.get('oshiro_id')
        
        # 管理者の担当城IDと、URLのIDが一致するか
        if admin.oshiro_info.id != oshiro_id:
            raise PermissionDenied
            
        return super().dispatch(request, *args, **kwargs)


def _get_or_404(model_cls, **kwargs):
    try:
        return model_cls.objects.get(**kwargs)
    except model_cls.DoesNotExist:
        raise Http404(f"{model_cls.__name__} not found")

# --- Viewクラス ---

class OshiroStampListView(AdminOshiroRequiredMixin,LoginRequiredMixin,View):
    """お城スタンプ一覧"""
    def get(self, request):
        # OneToOneの関係にあるお城情報もまとめて取得
        stamps = OshiroStampInfo.objects.all().select_related('oshiro_info').order_by("id")
        return render(request, "oshiro_stamp_list.html", {"stamps": stamps})



class OshiroStampRegistarView(AdminOshiroRequiredMixin,LoginRequiredMixin,View):
    """お城スタンプ登録"""

    def get(self, request):
        oshiro_list = OshiroInfo.objects.order_by("id")
        return render(request, "oshiro_stamp_registar.html", {
            "oshiro_list": oshiro_list
        })

    def post(self, request):
        if request.POST.get("cancel"):
            return redirect("admin_oshiro_stamp:oshiro_stamp_list")

        oshiro_id = request.POST.get("oshiro_id")
        stamp_name = request.POST.get("stamp_name")
        stamp_image = request.FILES.get("stamp_image")

        # 入力チェック
        if not oshiro_id or not stamp_name or not stamp_image:
            oshiro_list = OshiroInfo.objects.order_by("id")
            return render(request, "oshiro_stamp_registar.html", {
                "oshiro_list": oshiro_list,
                "error": "すべての項目を入力してください"
            })

        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        admin, created = Admin.objects.get_or_create(
            account=request.user
        )
        OshiroStampInfo.objects.create(
            oshiro_info=oshiro,
            admin=admin,
            stamp_name=stamp_name,
            oshiro_stamp_image=stamp_image
        )

        return redirect("admin_oshiro_stamp:oshiro_stamp_registar_success")

class OshiroStampRegistarSuccessView(AdminOshiroRequiredMixin,LoginRequiredMixin,TemplateView):
    template_name = "oshiro_stamp_registar_success.html"



class OshiroStampUpdateView(AdminOshiroRequiredMixin,LoginRequiredMixin,View):
    """お城スタンプ更新"""

    def get(self, request, stamp_id):
        stamp = _get_or_404(OshiroStampInfo, id=stamp_id)
        oshiro_list = OshiroInfo.objects.order_by("id")
        return render(request, "oshiro_stamp_update.html", {
            "stamp": stamp,
            "oshiro_list": oshiro_list
        })

    def post(self, request, stamp_id):
        if request.POST.get("cancel"):
            return redirect("admin_oshiro_stamp:oshiro_stamp_list")

        stamp = _get_or_404(OshiroStampInfo, id=stamp_id)

        oshiro_id = request.POST.get("oshiro_id")
        stamp_name = request.POST.get("stamp_name")
        stamp_image = request.FILES.get("stamp_image")

        # 入力チェック
        if not oshiro_id or not stamp_name:
            oshiro_list = OshiroInfo.objects.order_by("id")
            return render(request, "oshiro_stamp_update.html", {
                "stamp": stamp,
                "oshiro_list": oshiro_list,
                "error": "お城とスタンプ名は必須項目です"
            })

        oshiro = get_object_or_404(OshiroInfo, id=oshiro_id)
        stamp.oshiro_info = oshiro
        stamp.stamp_name = stamp_name
        if stamp_image:
            stamp.oshiro_stamp_image = stamp_image
        stamp.save()

        return redirect("admin_oshiro_stamp:oshiro_stamp_registar_success")

