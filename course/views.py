from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Course
from redis_ds.redis_list import RedisList
from redis import StrictRedis
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


class CourseView(APIView):
    """
    can be edited by staff only. The staff can fill in the details of
    the courses here. The course_info can contain the name of the
    lecturer in charge and some other anouncements

    Parameter for post:
        course_title: string
        course_code: string
        duration: int
        coure_info: text

    Parameter for put
        course_code: string
        course_title: string
        duration: int
        coure_info: text

    Parameter for delete
        course_code: string

    """
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get(self, request):
        return Response(Course.objects.all().values())

    def post(self, request):
        Course.objects.create(course_title=request.POST.get('course_title'),
                              course_code=request.POST.get('course_code').upper(),
                              duration=int(request.POST.get('duration')), course_info=request.POST.get('course_info')
        )
        return Response({'success': 'course registered'})

    def put(self, request):
        Course.objects.filter(course_code=request.data['course_code']).update(course_title=request.data['course_title'],
                                                                              duration=int(request.data['duration']),
                                                                              course_info=request.data['course_info']
        )
        return Response({'success': 'course updated'})

    def delete(self, request):
        course = Course.objects.filter(course_code=request.data['course_code']).delete()
        return Response({'success': 'course deleted'})


class CanTakeCourse(APIView):
    """
    can be edited by staff only. The excel file will be uploaded into
    the app and the app will extract the matric_no of registered students
    then it will call the API

    Parameters
        course_code: string
        can_take_course: a list of matric_nos that registered for the course
    """

    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    parser_classes = (JSONParser,)


    def get(self, request, **kwargs):
        redis_can_take_course = RedisList(kwargs['course_code'])
        return Response(redis_can_take_course[:])

    def post(self, request):
        key = request.data['course_code']

        r = StrictRedis(host='localhost', port=6379, db=0)
        r.delete(key)

        redis_can_take_course = RedisList(key)
        can_take_course = set(request.data['can_take_course'])
        for item in can_take_course:
            redis_can_take_course.append(item.upper())

        return Response({'success': 'can_take_course'})


@api_view(['GET'])
def get_time_left(request, course_code):
    """
        It returns time left in seconds
        Parameter
        course_code: string, it is added to the url
    """
    r = StrictRedis()
    ttl = r.ttl('active_class:{}'.format(course_code))

    return Response(ttl)