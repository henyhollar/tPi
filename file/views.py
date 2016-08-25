# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Document

from course.models import Course
import os
from django.conf import settings
from django.http import HttpResponse
from path import Path


class FileUploadView(APIView):
    """
    this attribute must be there on the form at the frontend enctype="multipart/form-data" for request.FILES
    or just use the normal request.data['file]
    """

    parser_classes = (FormParser, MultiPartParser,)
    #permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, **kwargs):
        course = Course.objects.get(course_code=kwargs.get('course_code'))
        documents = Document.objects.filter(course=course).values('file_name', 'size', 'date', 'file_type')

        return Response(documents)

    def post(self, request, **kwargs):
        course = Course.objects.get(course_code=kwargs.get('course_code'))
        file_obj = request.FILES['file']
        file_type = kwargs.get('file_type')

        doc = Document.objects.create(document=file_obj, course=course, size=file_obj.size, file_type=file_type)
        doc.save()

        return Response('File upload successful')

    def delete(self, request, **kwargs):
        filename = kwargs.get('file_name')
        course_code = kwargs.get('course_code')
        try:
            file_path = Document.objects.get(file_name=filename, document='{}/{}'.format(course_code, filename))
        except Document.DoesNotExist:
            return Response('File not in the database')
        os.remove(settings.MEDIA_ROOT+'{}'.format(file_path.document))
        file_path.delete()

        return Response('File delete successful')


def pdf_view(request, **kwargs):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_base_dir = Path(base_dir)
    path_to_pdf_file = path_base_dir.joinpath('media/{}/{}'.format(kwargs.get('course_code'), kwargs.get('file_name')))
    with open(path_to_pdf_file, 'r') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        #response['Content-Disposition'] = 'filename=some_file.pdf'
        response['Content-Disposition'] = 'inline;filename={}'.format(kwargs.get('file_name'))
        return response
