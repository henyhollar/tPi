from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from redis import StrictRedis
from course.models import Course
from rest_framework.authtoken.models import Token
from .permissions import CanTakeCourse
from .serializers import AttendanceSerializer

from datetime import datetime
from .models import Attendance

from django.contrib.auth import get_user_model
from django.core.exceptions import MultipleObjectsReturned

User = get_user_model()


class Get_Who_Attended(APIView):
    """
    this class if for the staff to call. It returns the marked attendance with the user information
    the parameters are:
        course_code: string
        date: string
    """

    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get(self, request, **kwargs):
        attendance = []
        attend = Attendance.objects.filter(course_code=kwargs['course_code'])
        if all([kwargs.has_key('year'), kwargs.has_key('month'), kwargs.has_key('day')]):
            date_str = '{} {} {}'.format(kwargs['year'], kwargs['month'], kwargs['day'])
            date = datetime.date(datetime.strptime(date_str, '%Y %b %d'))
            attend = attend.filter(date=date)
        for att in attend:
            attendance.append({'matric_no': att.user.identity,
                               'date': att.date,
                               'timestamp': att.timestamp,
                               'course_code': att.course_code
            })

        return Response(attendance)


class AttendanceView(APIView):
    """
    the parameters are:
        matric_no: string
        status: boolean
        course_code: string
        duration: integer
    """
    permission_classes = (permissions.IsAuthenticated,)# CanTakeCourse)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            #duration = request.POST.get('duration')
            #equest.session.set_expiry(duration*3600) set the expiry of the token
            return Response({'success': 'Attendance marked!'})

        return Response(serializer.errors)


class ActiveClass(APIView):
    """
    This section will give the class available or return none when called
    Parameters required are:
    course_code: string
    duration: integer
    """

    permission_classes = (permissions.IsAuthenticated,)

    redis_key = 'active_class:'

    def get(self, request):
        r = StrictRedis(host='localhost', port=6379, db=0)
        course_code = r.keys('active_class:*')
        course_code = course_code[0].split(':')[1] if len(course_code) > 0 else ''
        if not course_code:
            return Response('There is no active course!')
        try:
            course = Course.objects.filter(course_code=course_code)
        except Course.DoesNotExist:
            return Response('There is no course listed yet!')
        return Response(course.values())

    def post(self, request):
        course_code = request.POST.get('course_code')
        duration = int(request.POST.get('duration'))

        r = StrictRedis(host='localhost', port=6379, db=0)
        r.set('{}{}'.format(self.redis_key, course_code), course_code)
        r.expire('{}{}'.format(self.redis_key, course_code), duration*3600)

        return Response({'success': 'active_class stored'})


class StopActiveClass(APIView):
    """
    This section will stop an active class and logs all the students out
    Parameters required are:
    course_code: string
    """

    permission_classes = (permissions.IsAuthenticated,)

    redis_key = 'active_class:'

    def get(self, request):
        r = StrictRedis(host='localhost', port=6379, db=0)
        r.delete(r.keys('active_class:*')[0])
        try:
            staff = User.objects.get(is_staff=True)
            Token.objects.all().exclude(user=staff).delete()
        except MultipleObjectsReturned:
            #save message in redis and notify the admin at log in
            pass    # warn the admin of multiple staff entry possibly due to breach of password

        return Response('Class ends successfully')


