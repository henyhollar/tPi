# -*- coding: utf-8 -*-
from django.db import models
from course.models import Course


def file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/course_code/<filename>
    if instance.file_name == 'new':
        instance.file_name = filename   # truncate len
    else:
        filename = instance.file_name

    print filename
    path = '{0}/{1}'.format(instance.course.course_code, filename)
    print path, instance.document

    try:
        Document.objects.get(file_name=filename)
        raise Exception('File name already exists')
    except Document.DoesNotExist:
        return path


class Document(models.Model):
    file_name = models.CharField(max_length=100, default='new')
    document = models.FileField(upload_to=file_path, blank=True)
    course = models.ForeignKey(Course)
    size = models.CharField(max_length=10)
    date = models.DateField(auto_now=True)

    def __unicode__(self):
        return "{}:{}:{}".format(self.file_name, self.size, self.date)