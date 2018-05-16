# -*- coding: utf-8 -*-
"""cashflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^course_list/', views.courses_list, name='courses_list'),
    url(r'^list_courses/', views.list_courses, name='list_courses'),
    url(r'^create_course/', views.create_course, name='create_course'),
    url(r'^user/', views.user, name='user'),
    url(r'^courses/', views.courses, name='courses'),
    url(r'^login/', views.login, name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^password/', views.password, name='password'),
    url(r'^video_content/', views.video_content, name='video_content'),
    url(r'^test_content/', views.test_content, name='test_content'),
    url(r'^statistical/', views.statistical, name='statistical'),
    url(r'^master/', views.master, name='master'),
    url(r'^manage_statistical/', views.managestatistical, name='manage_statistical'),

    url(r'^$', views.courses_list, name='courses_list'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
