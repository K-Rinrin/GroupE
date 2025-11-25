from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class AreaMapInfoListView(TemplateView):
    template_name = "area_map_info_list.html"

# 登録画面
class AreaMapInfoRegistarView(TemplateView):
    template_name = "area_map_info_registar.html"

# 登録完了画面
class AreaMapInfoRegistarSuccessView(TemplateView):
    template_name = "area_map_info_registar_success.html"



# 更新画面
class AreaMapInfoUpdateView(TemplateView):
    template_name = "area_map_info_update.html"

# 更新完了画面
class AreaMapInfoUpdateSuccessView(TemplateView):
    template_name = "area_map_info_update_success.html"



# 削除画面
class AreaMapInfoDeleteView(TemplateView):
    template_name = "area_map_info_delete.html"

# 削除完了画面
class AreaMapInfoDeleteSuccessView(TemplateView):
    template_name = "area_map_info_delete_success.html"
