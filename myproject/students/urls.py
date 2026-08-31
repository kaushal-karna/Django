from django.urls import path
from . import views

app_name = "students"
urlpatterns = [
    path('', views.student_display, name='student_display'),
    path('<int:student_id>/', views.student_detail, name='student_detail'),
    path('home/', views.students_home, name='students_home'),
    path('about/', views.students_about, name='students_about'),
    path('list/', views.students_list, name='students_list')
]