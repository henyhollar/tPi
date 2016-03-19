# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FileUploadParser

from .models import Document

from course.models import Course


class FileUploadView(APIView):
    """
    this attribute must be there on the form at the frontend enctype="multipart/form-data" for request.FILES
    or just use the normal request.data['file]
    """

    parser_classes = (FileUploadParser,)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, **kwargs):
        course = Course.objects.get(course_code=kwargs.get('course_code'))
        documents = Document.objects.filter(course=course).values_list('document')

        return Response(documents)

    def post(self, request, **kwargs):
        course = Course.objects.get(course_code=kwargs.get('course_code'))
        file_obj = request.FILES['file']
        note = request.data.get('note', None)
        doc = Document.objects.create(document=file_obj, course=course, note=note)
        doc.save()

        return Response('File upload successful')


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
