from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.http import Http404
from datetime import datetime
from django.utils import timezone
import json

from .models import BasicInfo
from operator_oshiro_info.models import OshiroInfo


def _safe_int(value, default=0):
    if value is None or str(value).strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _parse_stamp_map(raw_text):
    if raw_text is None or raw_text.strip() == "":
        return {}
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {}


def _get_or_404(model_cls, **kwargs):
    try:
        return model_cls.objects.get(**kwargs)
    except model_cls.DoesNotExist:
        raise Http404(f"{model_cls.__name__} not found")


class BasicInfoListView(View):
    def get(self, request):
        # 1. ログイン中の管理者のプロフィールを取得
        # LoginRequiredMixinなどを使っている前提ですが、念のためチェック
        if not hasattr(request.user, 'admin_profile'):
            return render(request, "basic_info_list.html", {"rows": []})
        
        admin_profile = request.user.admin_profile

        # 2. 担当しているお城（1〜5）をリスト化（Noneを除外）
        managed_castle_ids = [
            admin_profile.oshiro_management1_id,
            admin_profile.oshiro_management2_id,
            admin_profile.oshiro_management3_id,
            admin_profile.oshiro_management4_id,
            admin_profile.oshiro_management5_id,
        ]
        managed_castle_ids = [cid for cid in managed_castle_ids if cid is not None]

        # 3. 担当お城のIDリストに含まれるOshiroInfoのみ取得
        oshiros = OshiroInfo.objects.filter(id__in=managed_castle_ids).order_by("id")

        rows = []
        for oshiro in oshiros:
            basic = BasicInfo.objects.filter(oshiro_info=oshiro).first()
            rows.append({"oshiro": oshiro, "basic": basic})

        return render(request, "basic_info_list.html", {"rows": rows})

class BasicInfoUpdateView(View):
    def get(self, request):
        oshiro_id = request.GET.get("oshiro_id")
        if not oshiro_id:
            return render(request, "basic_info_update.html", {"error": "必要情報を入力してください"})

        oshiro = _get_or_404(OshiroInfo, id=oshiro_id)
        basic = BasicInfo.objects.filter(oshiro_info=oshiro).first()

        return render(request, "basic_info_update.html", {"oshiro": oshiro, "basic": basic})

    def post(self, request):
        if request.POST.get("cancel"):
            return redirect("admin_basic_info:basic_info_list")

        oshiro_id = request.POST.get("oshiro_id")
        if not oshiro_id:
            return render(request, "basic_info_update.html", {"error": "必要情報を入力してください"})

        oshiro = _get_or_404(OshiroInfo, id=oshiro_id)

        basic = BasicInfo.objects.filter(oshiro_info=oshiro).first()
        if basic is None:
            basic = BasicInfo(oshiro_info=oshiro)

        # 必須項目
        admission_raw = request.POST.get("admission")
        opening_raw = request.POST.get("business_opening_hours")  # HH:MM
        closing_raw = request.POST.get("business_closing_hours")  # HH:MM
        access_info = request.POST.get("access_info")

        if (not admission_raw) or (not opening_raw) or (not closing_raw) or (not access_info):
            return render(
                request,
                "basic_info_update.html",
                {"oshiro": oshiro, "basic": basic, "error": "必要情報を入力してください"},
            )

        # 入場料
        basic.admission = _safe_int(admission_raw, default=0)

        # 営業時間（HH:MM → DateTimeField）
        today = timezone.localdate()

        try:
            open_time = datetime.strptime(opening_raw, "%H:%M").time()
            close_time = datetime.strptime(closing_raw, "%H:%M").time()
        except ValueError:
            return render(
                request,
                "basic_info_update.html",
                {"oshiro": oshiro, "basic": basic, "error": "必要情報を入力してください"},
            )

        basic.business_opening_hours = timezone.make_aware(datetime.combine(today, open_time))
        basic.business_closing_hours = timezone.make_aware(datetime.combine(today, close_time))

        # アクセス情報
        basic.access_info = access_info

        # 任意項目
        basic.highlights = request.POST.get("highlights") or ""
        basic.gojoin = request.POST.get("gojoin")

        # 画像（選択された時だけ更新）
        highlights_img = request.FILES.get("highlights_img")
        if highlights_img:
            basic.highlights_img = highlights_img

        gojoin_stamp = request.FILES.get("gojoin_stamp")
        if gojoin_stamp:
            basic.gojoin_stamp = gojoin_stamp

        # stamp_map（画面で編集しない：hiddenで来る想定）
        stamp_map_raw = request.POST.get("stamp_map")
        basic.stamp_map = _parse_stamp_map(stamp_map_raw)

        basic.save()

        return redirect("admin_basic_info:basic_info_update_success")


class BasicInfoUpdateSuccessView(TemplateView):
    template_name = "basic_info_update_success.html"
