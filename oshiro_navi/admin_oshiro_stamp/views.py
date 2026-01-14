from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class OshiroStampListView(TemplateView):
    template_name = "oshiro_stamp_list.html"

class OshiroStampRegistarView(TemplateView):
    template_name = "oshiro_stamp_registar.html"

class OshiroStampRegistarSuccessView(TemplateView):
    template_name = "oshiro_stamp_registar_success.html"


