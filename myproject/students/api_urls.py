from django.urls import path
from . import views

app_name='students_api'

urlpatterns = [
    # API PATH  
    path('student-list/', views.student_list, name='student_list')

]