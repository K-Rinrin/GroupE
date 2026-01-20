from django.urls import path

from .views import *

app_name = "user_model_course"

urlpatterns = [ 

    # 検索画面
    path('modelcoursechoose/', UsermodelCourseChooseView.as_view(), name='modelcoursechoose'),

    # 検索結果一覧画面
    path('modelcourselist/', UserModelCourseListView.as_view(), name='modelcourselist'),

    # 詳細画面
    path('modelcoursedetail/', UserModelCourseDetailView.as_view(), name='modelcoursedetail'), 

   
]
