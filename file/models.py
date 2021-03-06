# -*- coding: utf-8 -*-
from django.db import models
from course.models import Course


class SlideConverterError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/course_code/<filename>
    if instance.file_name == 'new':
        instance.file_name = filename   # truncate len
    else:
        filename = instance.file_name

    path = '{0}/{1}'.format(instance.course.course_code, filename)

    try:
        Document.objects.get(file_name=filename)
        raise SlideConverterError('')
    except Document.DoesNotExist:
        return path


class Document(models.Model):
    file_name = models.CharField(max_length=100, default='new')
    file_type = models.CharField(max_length=20)
    document = models.FileField(upload_to=file_path, blank=True)
    course = models.ForeignKey(Course)
    size = models.CharField(max_length=10)
    date = models.DateField(auto_now=True)

    def __unicode__(self):
        return "{}:{}:{}".format(self.file_name, self.size, self.date)