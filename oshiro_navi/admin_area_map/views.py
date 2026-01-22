# admin_area_map/views.py
import json
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from .models import AreaMapInfo
from .forms import AreaMapInfoForm
from django.core.serializers.json import DjangoJSONEncoder
from admin_basic_info.models import BasicInfo

TSURUGAJO_CENTER = {"lat": 37.4879, "lng": 139.9290, "zoom": 16}

def _get_map_center_from_basicinfo(basic_info_id: int):
    """
    BasicInfo → OshiroInfo の緯度経度を見て map_center を作る
    無い場合は TSURUGAJO_CENTER にフォールバック
    """
    basic = get_object_or_404(
        BasicInfo.objects.select_related("oshiro_info"),
        pk=basic_info_id
    )
    oshiro = basic.oshiro_info

    lat = oshiro.latitude if oshiro.latitude is not None else TSURUGAJO_CENTER["lat"]
    lng = oshiro.longitude if oshiro.longitude is not None else TSURUGAJO_CENTER["lng"]
    zoom = TSURUGAJO_CENTER["zoom"]

    return {"lat": lat, "lng": lng, "zoom": zoom, "oshiro_name": oshiro.oshiro_name}


class AreaMapTopView(TemplateView):
    template_name = "area_map_top.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # 管理者プロフィールがないなら空表示
        if not hasattr(self.request.user, "admin_profile"):
            ctx["basic_infos"] = BasicInfo.objects.none()
            return ctx

        ap = self.request.user.admin_profile

        managed_castle_ids = [
            ap.oshiro_management1_id,
            ap.oshiro_management2_id,
            ap.oshiro_management3_id,
            ap.oshiro_management4_id,
            ap.oshiro_management5_id,
        ]
        managed_castle_ids = [cid for cid in managed_castle_ids if cid is not None]

        # ✅ BasicInfo を「担当城の OshiroInfo」に絞る
        ctx["basic_infos"] = (
            BasicInfo.objects
            .select_related("oshiro_info")
            .filter(oshiro_info_id__in=managed_castle_ids)
            .order_by("id")
        )
        return ctx


class AreaMapInfoListView(ListView):
    template_name = "area_map_info_list.html"
    context_object_name = "maps"
    model = AreaMapInfo

    def get_queryset(self):
        return AreaMapInfo.objects.filter(
            basic_info_id=self.kwargs["basic_info_id"]
        ).order_by("-id")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        basic_info_id = self.kwargs["basic_info_id"]
        ctx["basic_info_id"] = basic_info_id

        center = _get_map_center_from_basicinfo(basic_info_id)
        ctx["map_center"] = {"lat": center["lat"], "lng": center["lng"], "zoom": center["zoom"]}
        ctx["oshiro_name"] = center["oshiro_name"]

        # ★追加：JS用データ（表なしでもピンを描ける）
        ctx["maps_json"] = json.dumps([
            {
                "id": m.id,
                "icon_name": m.icon_name,
                "lat": m.latitude,
                "lng": m.longitude,
                "image_url": (m.icon_image.url if m.icon_image else ""),
                "update_url": reverse("admin_area_map:area_map_info_update", kwargs={"pk": m.id}),
            }
            for m in ctx["maps"]
        ], cls=DjangoJSONEncoder)

        return ctx

class AreaMapInfoRegistarView(CreateView):
    template_name = "area_map_info_registar.html"
    model = AreaMapInfo
    form_class = AreaMapInfoForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        basic_info_id = self.kwargs["basic_info_id"]
        ctx["basic_info_id"] = basic_info_id

        center = _get_map_center_from_basicinfo(basic_info_id)
        ctx["map_center"] = {"lat": center["lat"], "lng": center["lng"], "zoom": center["zoom"]}
        ctx["oshiro_name"] = center["oshiro_name"]

        return ctx

    def form_valid(self, form):
        basic_info = get_object_or_404(BasicInfo, pk=self.kwargs["basic_info_id"])
        pins_json = (self.request.POST.get("pins_json") or "").strip()
        uploaded_img = self.request.FILES.get("icon_image")

        if pins_json:
            try:
                pins = json.loads(pins_json)
            except json.JSONDecodeError:
                form.add_error(None, "pins_json の形式が不正です。")
                return self.form_invalid(form)

            if not isinstance(pins, list) or len(pins) == 0:
                form.add_error(None, "地図をクリックしてピンを追加してください。")
                return self.form_invalid(form)

            objs = []
            for p in pins:
                category = (p.get("category") or "").strip()
                lat = p.get("lat")
                lng = p.get("lng")
                if not category or lat is None or lng is None:
                    continue

                obj = AreaMapInfo(
                    basic_info=basic_info,
                    icon_name=category,
                    latitude=float(lat),
                    longitude=float(lng),
                )
                if uploaded_img:
                    obj.icon_image = uploaded_img
                objs.append(obj)

            if len(objs) == 0:
                form.add_error(None, "有効なピンがありません。")
                return self.form_invalid(form)

            for obj in objs:
                obj.save()

            return redirect(self.get_success_url())

        form.instance.basic_info = basic_info
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "admin_area_map:area_map_info_registar_success",
            kwargs={"basic_info_id": self.kwargs["basic_info_id"]}
        ) + f"?basic_info_id={self.kwargs['basic_info_id']}"


class AreaMapInfoRegistarSuccessView(TemplateView):
    template_name = "area_map_info_registar_success.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["basic_info_id"] = self.kwargs["basic_info_id"]
        return ctx


# ※ 更新/削除を urls.py に書いているなら、ここも必要
class AreaMapInfoUpdateView(UpdateView):
    template_name = "area_map_info_update.html"
    model = AreaMapInfo
    form_class = AreaMapInfoForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        basic_info_id = self.object.basic_info_id
        ctx["basic_info_id"] = basic_info_id

        center = _get_map_center_from_basicinfo(basic_info_id)
        ctx["map_center"] = {"lat": center["lat"], "lng": center["lng"], "zoom": center["zoom"]}
        ctx["oshiro_name"] = center["oshiro_name"]

        return ctx

    def get_success_url(self):
        return reverse("admin_area_map:area_map_info_update_success", kwargs={"pk": self.object.pk})


class AreaMapInfoUpdateSuccessView(TemplateView):
    template_name = "area_map_info_update_success.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = get_object_or_404(AreaMapInfo, pk=self.kwargs["pk"])
        ctx["basic_info_id"] = obj.basic_info_id
        return ctx


class AreaMapInfoDeleteView(DeleteView):
    template_name = "area_map_info_delete.html"
    model = AreaMapInfo

    def get_success_url(self):
        return reverse(
            "admin_area_map:area_map_info_delete_success",
            kwargs={"basic_info_id": self.object.basic_info_id}
        )


class AreaMapInfoDeleteSuccessView(TemplateView):
    template_name = "area_map_info_delete_success.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["basic_info_id"] = self.kwargs["basic_info_id"]
        return ctx
