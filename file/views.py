# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Document

from course.models import Course
import os
from django.conf import settings

class FileUploadView(APIView):
    """
    this attribute must be there on the form at the frontend enctype="multipart/form-data" for request.FILES
    or just use the normal request.data['file]
    """

    parser_classes = (FormParser, MultiPartParser,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, **kwargs):
        course = Course.objects.get(course_code=kwargs.get('course_code'))
        documents = Document.objects.filter(course=course).values('file_name', 'size', 'date')

        return Response(documents)

    def post(self, request, **kwargs):
        course = Course.objects.get(course_code=kwargs.get('course_code'))
        file_obj = request.FILES['file']
        doc = Document.objects.create(document=file_obj, course=course, size=file_obj.size)
        doc.save()

        return Response('File upload successful')

    def delete(self, request, **kwargs):
        print kwargs.get('file_name')
        Document.objects.get(file_name=kwargs.get('file_name')).delete()
        os.remove(os.path.join(settings.MEDIA_ROOT, kwargs.get('file_name')))

        return Response('File delete successful')





#class FileUploadView(APIView):
#    parser_classes = (FileUploadParser, )
#    permission_classes = (IsAuthenticated, IsAdminUser)
#
#    def post(self, request, **kwargs, format='pdf'):
#        up_file = request.FILES['file']
#        destination = open('/Users/Username/{}'.format(**kwargs['course_code']) + up_file.name, 'wb+')
#        for chunk in up_file.chunks():
#            destination.write(chunk)
#            destination.close()
#
#        # ...
#        # do some stuff with uploaded file
#        # ...
#        return Response(up_file.name, status.HTTP_201_CREATED)
