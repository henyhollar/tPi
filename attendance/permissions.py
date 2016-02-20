from rest_framework import permissions
from redis_ds.redis_list import RedisList


class CanTakeCourse(permissions.BasePermission):
    
    message = 'You are not allowed to mark attendance for this course'

    def has_permission(self, request, view):
        
        redis_can_take_course = RedisList(request.data['course_code'])#course_code
        if request.data['matric_no'] in redis_can_take_course[:]:
			return True
        else:
			return False
