# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = [
    url(r'^upload/(?P<course_code>[A-Z0-9]{6})/(?P<file_type>[a-z]+)/$', views.FileUploadView.as_view(), name='upload'),
    url(r'^list/(?P<course_code>[A-Z0-9]{6})/$', views.FileUploadView.as_view(), name='list'),
    url(r'^delete_file/(?P<course_code>[A-Z0-9]{6})/(?P<file_name>[a-zA-Z0-9. ]+)/$', views.FileUploadView.as_view(), name='delete'),
    url(r'^view_pdf/(?P<course_code>[A-Z0-9]{6})/(?P<file_name>[a-z]+)/$', views.pdf_view, name='pdf_view'),

]