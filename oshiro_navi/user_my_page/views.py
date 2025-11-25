from django.shortcuts import render
from django.views.generic.base import TemplateView


class MypageView(TemplateView):
    template_name = "mypage.html"

class MyListRegistarView(TemplateView):
    template_name = "my_list_registar.html"

class MyListDeleteCheckView(TemplateView):
    template_name = "my_list_delete_check.html"

class OshiroStampRegistar(TemplateView):
    template_name = "oshiro_stamp_registar.html"

class UserProfileUpdateView(TemplateView):
    template_name = "user_profile_update.html"

class UserProfileView(TemplateView):
    template_name = "user_profile.html"

class MyListDeleteView(TemplateView):
    template_name = "my_list_delete.html"