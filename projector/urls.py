# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = [
    url(r'^presentation/$', views.presentation, name='presentation'),
    url(r'^convert_to_slide/$', views.convert_to_slide, name='presentation'),
]

