from django.shortcuts import render
from django.views.generic.base import TemplateView


class UserModelCourseListView(TemplateView):
    template_name = "model_course_list.html"

class UserModelCourseDetailView(TemplateView):
    template_name = "model_course_detail.html"

class UserModelCourseAfterSearchView(TemplateView):
    template_name = "model_course_after_search.html"

class UsermodelCourseChooseView(TemplateView):
    template_name = "model_course_choose.html"


