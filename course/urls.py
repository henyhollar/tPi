from django.conf.urls import url

from .import views


urlpatterns = [
    url(r'^$', views.CourseView.as_view(), name='course'),
    url(r'^can_take_course/$', views.CanTakeCourse.as_view(), name='post_can_take_course'),
    url(r'^can_take_course/(?P<course_code>[A-Z0-9]{6})/$', views.CanTakeCourse.as_view(), name='get_can_take_course'),
    url(r'^time_left/(?P<course_code>[A-Z0-9]{6})/$', views.get_time_left, name='get_time_left'),

]
