import json

from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView

from .models import AreaMapInfo
from .forms import AreaMapInfoForm
from admin_basic_info.models import BasicInfo

TSURUGAJO_CENTER = {"lat": 37.4879, "lng": 139.9290, "zoom": 16}


class AreaMapTopView(TemplateView):
    template_name = "area_map_top.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["basic_infos"] = BasicInfo.objects.select_related("oshiro_info").all().order_by("id")
        return ctx


class AreaMapInfoListView(ListView):
    template_name = "area_map_info_list.html"
    context_object_name = "maps"
    model = AreaMapInfo

    def get_queryset(self):
        return AreaMapInfo.objects.filter(basic_info_id=self.kwargs["basic_info_id"]).order_by("-id")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["basic_info_id"] = self.kwargs["basic_info_id"]
        ctx["map_center"] = TSURUGAJO_CENTER
        return ctx


class AreaMapInfoRegistarView(CreateView):
    template_name = "area_map_info_registar.html"
    model = AreaMapInfo
    form_class = AreaMapInfoForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["basic_info_id"] = self.kwargs["basic_info_id"]
        ctx["map_center"] = TSURUGAJO_CENTER
        return ctx

    def form_valid(self, form):
        basic_info = get_object_or_404(BasicInfo, pk=self.kwargs["basic_info_id"])

        pins_json = self.request.POST.get("pins_json", "").strip()
        if not pins_json:
            form.add_error(None, "地図をクリックしてピンを追加してください。")
            return self.form_invalid(form)

        try:
            pins = json.loads(pins_json)
        except json.JSONDecodeError:
            form.add_error(None, "ピン情報の読み取りに失敗しました。")
            return self.form_invalid(form)

        uploaded_image = form.cleaned_data.get("icon_image")

        objs = []
        for p in pins:
            category = p.get("category")
            lat = p.get("lat")
            lng = p.get("lng")
            if category is None or lat is None or lng is None:
                continue

            obj = AreaMapInfo(
                basic_info=basic_info,
                icon_name=str(category),
                latitude=float(lat),
                longitude=float(lng),
            )
            if uploaded_image:
                obj.icon_image = uploaded_image
            objs.append(obj)

        if not objs:
            form.add_error(None, "有効なピンがありません。")
            return self.form_invalid(form)

        AreaMapInfo.objects.bulk_create(objs)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "admin_area_map:area_map_info_registar_success",
            kwargs={"basic_info_id": self.kwargs["basic_info_id"]}
        )


class AreaMapInfoRegistarSuccessView(TemplateView):
    template_name = "area_map_info_registar_success.html"


class AreaMapInfoUpdateView(UpdateView):
    template_name = "area_map_info_update.html"
    model = AreaMapInfo
    form_class = AreaMapInfoForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["basic_info_id"] = self.object.basic_info_id
        ctx["map_center"] = TSURUGAJO_CENTER
        return ctx

    def get_success_url(self):
        return reverse("admin_area_map:area_map_info_update_success", kwargs={"pk": self.object.pk})


class AreaMapInfoUpdateSuccessView(TemplateView):
    template_name = "area_map_info_update_success.html"


class AreaMapInfoDeleteView(DeleteView):
    template_name = "area_map_info_delete.html"
    model = AreaMapInfo

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["basic_info_id"] = self.object.basic_info_id
        return ctx

    def get_success_url(self):
        return reverse("admin_area_map:area_map_info_delete_success")


class AreaMapInfoDeleteSuccessView(TemplateView):
    template_name = "area_map_info_delete_success.html"
