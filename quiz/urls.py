# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views

urlpatterns = [
    url(r'^upload_quiz/(?P<course_code>[A-Z0-9]{6})/(?P<file_name>[a-zA-Z0-9. ]+)/$', views.upload_quiz, name='upload_quiz'),
    url(r'^submit_quiz/$', views.SubmitQuiz.as_view(), name='submit_quiz'),
    url(r'^take_quiz/(?P<course_code>[A-Z0-9]{6})/(?P<topic>[a-zA-Z0-9. ]+)/(?P<no_of_questions>[0-9]+)/$', views.take_quiz, name='take_quiz'),
    url(r'^get_topics/(?P<course_code>[A-Z0-9]{6})/$', views.get_topics, name='get_topics'),

]

