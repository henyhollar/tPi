from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TeacherPiUser, MacAddress, DefaultPass
from redis_ds.redis_list import RedisList
from redis import StrictRedis

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherPiUser
        fields = ('identity', )

    def validate_identity(self, value):
        identity = value.upper()

        if len(identity) in [8, 12, 14]:
            try:
                User.objects.get(identity=identity)
                raise serializers.ValidationError('Matric No. already exists. Please report to the admin')
            except User.DoesNotExist:
                return identity
        else:
            raise serializers.ValidationError('Matric No. is not valid')

    #validate the mac address here
    def validate(self, data):
        try:
            MacAddress.objects.get(mac_add=self.context['mac_add'])
            raise serializers.ValidationError('MAC address conflicting or missing, please contact the admin')
        except MacAddress.DoesNotExist:
            return data

    def save(self):
        user = User.objects.create_user(self.validated_data['username'], self.validated_data['password'])
        user.identity = self.validated_data['identity']
        user.is_staff = True if self.context['user_type'] == 'staff' else False
        mac_add = MacAddress.objects.create(owner=user, mac_add=self.context['mac_add'])

        user.save()
        mac_add.save()


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherPiUser
        fields = ('identity', )

    def validate(self, attrs):
        username = self.context['identity'].replace('/', '')
        if self.context['user_type']=='student':
            password = 'teacherpiuser'
            r = StrictRedis(host='localhost', port=6379, db=0)
            course_code = r.keys('active_class:*')
            course_code = course_code[0].split(':')[1] if len(course_code) > 0 else ''
            if not course_code:
                raise serializers.ValidationError('There is no active class. Report to your lecturer')

            redis_can_take_course = RedisList(course_code)
            if self.context['identity'] not in redis_can_take_course[:]:
                raise serializers.ValidationError('There is no active class for this matric number')

        elif self.context['user_type']=='staff':
            d_password = DefaultPass.objects.get(id=1)
            if self.context['password'] == d_password.password:
                password = d_password.password
            else:
                raise serializers.ValidationError('Please report this case to the admin*')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs