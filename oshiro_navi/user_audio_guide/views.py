from django.shortcuts import render
from django.views.generic.base import TemplateView


# Create your views here.
class AudioGUideListView(TemplateView):
    template_name = "audio_guide_list.html"

class QrScanView(TemplateView):
    template_name = "qr_scan.html"