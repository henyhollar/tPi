from django.conf.urls import url

from .import views


urlpatterns = [
	url(r'^$', views.AttendanceView.as_view(), name='attendance'),
	url(r'^activeclass/$', views.ActiveClass.as_view(), name='active_class'),
    #url(r'^activeclass/(?P<course_code>[A-Z0-9]{6})/$', views.ActiveClass.as_view(), name='active_class_get'),
	url(r'^attendance_list/(?P<course_code>[A-Z0-9]{6})/$', views.Get_Who_Attended.as_view(), name='get_who_attended'),
    url(r'^attendance_list/(?P<course_code>[A-Z0-9]{6})/(?P<year>\d{4})/(?P<month>[A-Za-z]{3})/(?P<day>[0-9]{2})/$', views.Get_Who_Attended.as_view(), name='get_who_attended_with_date'),

]


#http://localhost:8000/attendance/attendance_list/EEE202/2016/Jan/02/