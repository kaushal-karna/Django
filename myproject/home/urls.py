from django.urls import path
from . import views

app_name = "home"
urlpatterns = [      
            path('', views.homepage, name="home_page"),  # Landing page
            path('dashboard/', views.dashboard, name="dashboard" ),
            path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
            path('profile/', views.profile_create, name='profile'),
                    
]