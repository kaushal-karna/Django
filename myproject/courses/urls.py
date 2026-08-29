from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_display, name='course_display'),
    path('home/', views.courses_home, name='courses_home'),
    path('about/', views.courses_about, name='courses_about'),
]