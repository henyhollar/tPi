# -*- coding: utf-8 -*-
from django.db import models
from course.models import Course


def file_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/course_code/<filename>
    return 'document/{0}/{1}'.format(instance.course.course_code, filename)


class Document(models.Model):
    notes = models.TextField(blank=True)
    document = models.FileField(upload_to=file_path, unique=True)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return "{}:{}:{}".format(self.user, self.course_code, self.date)