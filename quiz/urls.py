# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = [
    url(r'^upload_quiz/(?P<course_code>[A-Z0-9]{6})/(?P<file_name>[a-zA-Z0-9. ]+)/$', views.upload_quiz, name='upload_quiz'),
    url(r'^submit_quiz/$', views.SubmitQuiz.as_view(), name='submit_quiz'),
    url(r'^upload_quiz/(?P<course_code>[A-Z0-9]{6})/(?P<topic>[.]+)/(?P<no_of_questions>[0-9]+)/$', views.take_quiz, name='take_quiz'),

]

