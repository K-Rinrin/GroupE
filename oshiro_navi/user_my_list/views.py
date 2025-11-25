from django.shortcuts import render
from django.views.generic.base import TemplateView


class OshirolistView(TemplateView):
    template_name = "oshiro_list.html"

class OshiroInfoView(TemplateView):
    template_name = "oshiro_info.html"

class OshiroAfterSearchView(TemplateView):
    template_name = "oshiro_after_search.html"

class OshiroBasicInfoView(TemplateView):
    template_name = "oshiro_basic_info.html"

class OshiroReviewView(TemplateView):
    template_name = "user_review.html"