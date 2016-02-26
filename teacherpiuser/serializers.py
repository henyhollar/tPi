from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TeacherPiUser, MacAddress, DefaultPass
from redis_ds.redis_list import RedisList
from redis import StrictRedis

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
import re

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherPiUser
        fields = ('identity',)

    def validate_identity(self, value):
        identity = value.upper()

        if any([re.match(r"(([a-z]{2}/)[a-z\d]{5})", identity, re.I),
                re.match(r"([a-z]{3}/[\d]{4}/[\d]{3})", identity, re.I),
                re.match(r"([a-z\d]{4}/[\d]{2}/[a-z]{1}/[\d]{4})", identity, re.I)]):

            try:
                User.objects.get(identity=identity)
                raise serializers.ValidationError('Identity already exists. Please report to the admin')
            except User.DoesNotExist:
                return identity
        else:
            raise serializers.ValidationError('Identity is not valid')

    #validate the mac address here
    def validate(self, data):
        if self.context['mac_add']:
            try:
                MacAddress.objects.get(mac_add=self.context['mac_add'])
            except MacAddress.DoesNotExist:
                return data
        raise serializers.ValidationError('MAC address conflicting or missing, please contact the admin')

    def save(self):
        password = DefaultPass.objects.get(id=1).password if self.context['user_type'] == 'staff' else 'teacherpiuser'
        user = User.objects.create_user(self.validated_data['identity'].replace('/', ''), password=password)
        user.identity = self.validated_data['identity']
        user.is_staff = True if self.context['user_type'] == 'staff' else False
        mac_add = MacAddress.objects.create(owner=user, mac_add=self.context['mac_add'])

        user.save()
        mac_add.save()


class AuthTokenSerializer(serializers.Serializer):
    identity = serializers.CharField()

    def validate(self, value):
        username = value.get('identity').replace('/', '')

        if self.context['user_type']=='student':
            password = 'teacherpiuser'
            r = StrictRedis(host='localhost', port=6379, db=0)
            course_code = r.keys('active_class:*')
            course_code = course_code[0].split(':')[1] if len(course_code) > 0 else ''
            if not course_code:
                raise serializers.ValidationError('There is no active class')

            redis_can_take_course = RedisList(course_code)
            if self.context['identity'].upper() not in redis_can_take_course[:]:
                raise serializers.ValidationError('No class active for Matric number')

        elif self.context['user_type']=='staff':
            d_password = DefaultPass.objects.get(id=1)
            if self.context['password'] == d_password.password:
                password = d_password.password
            else:
                raise serializers.ValidationError('Please report this case to the admin*')

        if username and password:
            username = username.upper()
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                try:
                    User.objects.get(username=username)
                    raise serializers.ValidationError('Please choose the correct user type')
                except User.DoesNotExist:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        value['user'] = user
        return value