# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = [
    url(r'^upload/(?P<course_code>[A-Z0-9]{6})/$', views.FileUploadView.as_view(), name='upload'),
    url(r'^list/(?P<course_code>[A-Z0-9]{6})/$', views.FileUploadView.as_view(), name='list'),
]
