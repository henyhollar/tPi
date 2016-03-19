# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = [
    url(r'^upload/$', views.FileUploadView.as_view(), name='upload'),
    #url(r'^list/$', views.list, name='upload'),
]
