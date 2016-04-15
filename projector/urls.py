# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = [
    url(r'^presentation/$', views.presentation, name='presentation'),
]

