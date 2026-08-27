from django.urls import path
from . import views

urlpatterns = [      
            path('home/', views.home, name='home'),
            path('', views.homepage, name="homepage"), 
            path('about/', views.about, name='about'),
            path('students/<int:student_id>/', views.student_detail, name='student_detail'),
            path('students/', views.student_display, name='student_display'),
]