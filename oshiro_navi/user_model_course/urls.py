from django.urls import path

from .views import *

app_name = "user_model_course"

urlpatterns = [ 
    path('modelcourselist/', UserModelCourseListView.as_view(), name='modelcourselist'),
    path('modelcourseaftersearch/', UserModelCourseAfterSearchView.as_view(), name='modelcourseaftersearch'),
    path('modelcoursedetail/', UserModelCourseDetailView.as_view(), name='modelcoursedetail'), 
    path('modelcoursechoose/', UsermodelCourseChooseView.as_view(), name='modelcoursechoose'),
    
    
   
]
