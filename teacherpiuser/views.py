from rest_framework import generics, permissions, status, exceptions
from rest_framework.views import APIView
from serializers import RegisterSerializer, AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import parsers, renderers
from rest_framework.decorators import api_view

from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied

from django.contrib.auth import get_user_model
from .models import DefaultPass, MacAddress


from ipware.ip import get_ip
from subprocess import Popen, PIPE
from datetime import datetime
import re
import os



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
        serializer = RegisterSerializer(data=request.data, context={'mac_add': get_mac_add(request),
                                                                    'user_type': request.data['user_type']})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                                                                       'identity': request.data['identity']})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            mac_add = get_mac_add(request)
            try:
                mac = MacAddress.objects.get(mac_add=mac_add)
                print mac.owner, user
                print user == mac.owner
                if user == mac.owner:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                else:
                    raise PermissionDenied('Please use your device')
            except MacAddress.DoesNotExist:
                MacAddress.objects.create(owner=user, mac_add=mac_add)  # warn of silent registering of devices
        except Exception, e:
            if ["Unable to log in with provided credentials."] in serializer.errors.itervalues():
                view = RegisterView()
                view.post(request)
                user = User.objects.get(username=request.data['identity'].replace('/', '').upper())
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                raise e


obtain_auth_token = ObtainAuthToken.as_view()


def get_mac_add(request):
    #return '00:00:00:00:00'
    ip = get_ip(request)
    if ip is not None:
        pid = Popen(["arp", "-n", ip], stdout=PIPE)
        s = pid.communicate()[0]
        mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]  # use for matric no.

        return mac

    else:
        raise PermissionDenied('IP not accessible, please notify the admin')

@api_view(['GET'])
def house_keeping(request, **kwargs):
    print 'sudo date -s "{}"'.format(str(kwargs.get('timestamp')))
    os.system('sudo date -s "{}"'.format(str(kwargs.get('timestamp'))))

    return Response('Time set successful')