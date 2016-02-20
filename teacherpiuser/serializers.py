from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TeacherPiUser, MacAddress

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class meta:
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

        mac_add = MacAddress.objects.create(owner=user, mac_add=self.context['mac_add'])

        user.save()
        mac_add.save()



