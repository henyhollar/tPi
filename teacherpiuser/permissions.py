from rest_framework import permissions
#from .views import User
from ipware.ip import get_ip
from subprocess import Popen, PIPE
import re
from redis_ds.redis_list import RedisList
from redis import StrictRedis

from django.contrib.auth import get_user_model

User = get_user_model()


def get_mac_add(request):
    ip = get_ip(request)
    if ip is not None:
        pid = Popen(["arp", "-n", ip], stdout=PIPE)
        s = pid.communicate()[0]
        mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]
        print mac
        return mac


class MacAdd(permissions.BasePermission):
    
    message = 'Please use the device you registered with if you have registered or request to add more devices'

    def has_permission(self, request, view):
        mac_add = get_mac_add(request)
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return False
        if mac_add == user.mac_add:
            return True
        else:
            return False


class ActiveUser(permissions.BasePermission):

    message = 'None of your classes is active. Please complain to the admin in the case of an oversight'

    def has_permission(self, request, view):

        r = StrictRedis(host='localhost', port=6379, db=0)
        course_code = r.keys('active_class:*')
        course_code = course_code[0].split(':')[1] if len(course_code) > 0 else ''
        print course_code
        redis_can_take_course = RedisList(course_code)
        print redis_can_take_course
        if request.user.matric_no in redis_can_take_course[:]:
            return True
        else:
            return False


