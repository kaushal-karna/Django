"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import(
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# django restframework routers
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('courses/', include('courses.urls')),
    
    # DRF AUTHENTICATION VIEWS
    path('api-auth/', include('rest_framework.urls')),
    
    # Your  API URLS
    path('api/', include('students.api_urls')),
    path('api/', include('tasks.urls')),
    
    # DRF SPECTACULAR
    
    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    
    # Swagger UI
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
    
    # ReDoc
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc"
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )