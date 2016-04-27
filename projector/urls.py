# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = [
    url(r'^presentation/$', views.presentation, name='presentation'),
    url(r'^convert_to_slide/(?P<file_name>[a-zA-Z0-9]+)/$', views.convert_to_slide, name='slide'),
]

