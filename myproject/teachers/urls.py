from django.urls import path
from . import views

urlpatterns = [      
            path('', views.teachers_list, name='teachers_list'),  
            path('home/', views.teachers_home, name='teachers_home'),
            path('about/', views.teachers_about, name='teachers_about'),          
]