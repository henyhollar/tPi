from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Attendance
from datetime import datetime

User = get_user_model()


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ('course_code',)

    def validate(self, data):
        try:
            Attendance.objects.get(user=self.context['request'].user,
                                   course_code=data['course_code'],
                                   date= datetime.date(datetime.now()))
        except Attendance.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError('You can only mark attendance for a course just once')

        return data

    def save(self, **kwargs):
        assert self.instance is None, 'Cannot update users with CreateUserSerializer'
        Attendance.objects.create(user=self.context['request'].user, course_code=self.validated_data['course_code'].upper())


