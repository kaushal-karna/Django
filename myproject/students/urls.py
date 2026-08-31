from django.urls import path
from . import views

app_name='students'

urlpatterns = [
 
    path('student-list/', views.student_list, name='student_list'),
    path('index/', views.index, name='index'),
    path('student/', views.student_detail, name='student_details'),
   

]