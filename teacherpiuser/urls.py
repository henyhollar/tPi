from django.conf.urls import url

from .import views

"""
To login, the client will call /teacherpiuser/login/. This will return
the token in the response content. The client will build:
		{"Authorization": "Token 93442......."} 
and add it to the header of all subsequent requests.
	
"""

urlpatterns = [
    url(r'^login/$', views.obtain_auth_token),
    url(r'^logout/$', views.DeleteToken.as_view()),
]


