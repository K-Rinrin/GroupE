from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class AreaMapInfoListView(TemplateView):
    template_name = "area_map_info_list.html"
