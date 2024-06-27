"""testdj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from CuSell import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('templates/mainpage.html/', views.index),
    path('templates/registration.html/', views.reg),
    path('templates/login.html/', views.login),
    path('templates/error.html/', views.error),
    path('templates/profile.html/', views.profile),
    path('test_upload', views.test_upload),
    path('templates/post.html', views.post_mech),
    path('merchandise/<int:mid>', views.merchandise),
    path('templates/liked.html', views.my_liked),
    path(r'^static/(?P<path>.*)$', serve, {"document_root": settings.STATIC_ROOT})
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
