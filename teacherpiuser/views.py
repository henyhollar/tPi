from rest_framework import generics, permissions, status, exceptions
from rest_framework.views import APIView
from serializers import RegisterSerializer, AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import parsers, renderers
#from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied

from django.contrib.auth import get_user_model
from .models import DefaultPass, MacAddress

from ipware.ip import get_ip
from subprocess import Popen, PIPE
import re


User = get_user_model()


class RegisterView(APIView):

    """
    Parameters are:
        username: inferred from identity
        password: set internally
        identity: string
        user_type: string

        Check if the intending teacherpiuser has a class active before registering/login, if not return there is no active class
    """

    def post(self, request):
        #check if the intending user is a member of any class at all
        serializer = RegisterSerializer(data=request.data, context={'mac_add': get_mac_add(request),
                                                                    'user_type': request.data['user_type']})
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        raise Exception('Registration not successful')


class DeleteToken(APIView):
    """
    Call the logout with the REST delete method
    """

    def delete(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user.username)
        token = Token.objects.get(user=user)
        logout(request)
        token.delete()
        token.save()
        return Response('Sign-out successful')


class DeleteAllToken(APIView):
    """
    this should be called after the active class timed out.
    """

    def delete(self, request, *args, **kwargs):
        Token.objects.all().delete()
        return Response('All users logged out successfully')


class ObtainAuthToken(APIView):
    throttle_classes = ()   # set this
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        password = request.data.get('password', None)

        serializer = self.serializer_class(data=request.data, context={'user_type': request.data['user_type'],
                                                                       'password': password,
                                                                       'identity': request.data['identity'] })
        if serializer.is_valid():
            user = serializer.validated_data['user']
            mac_add = get_mac_add(request)
            try:
                mac = MacAddress.objects.get(mac_add=mac_add)
                if user == mac.owner:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                else:
                    raise PermissionDenied('Please use the devices registered for you')
            except MacAddress.DoesNotExist:
                user.macaddress_set(mac_add=mac_add)  # warn of silent registering of devices

        elif not serializer.is_valid() and serializer.errors['non_field_errors']==["Unable to log in with provided credentials."]:
            print serializer.errors
            view = RegisterView.as_view()
            view(request, *args, **kwargs)
            user = User.objects.get(username=request.data['username'])
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        return Response(serializer.errors)


obtain_auth_token = ObtainAuthToken.as_view()


def get_mac_add(request):
    ip = get_ip(request)
    if ip is not None:
        pid = Popen(["arp", "-n", ip], stdout=PIPE)
        s = pid.communicate()[0]
        mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]

        return mac

    else:
        raise PermissionDenied('IP not accessible, please notify the admin')
