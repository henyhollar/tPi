# -*- coding: utf-8 -*-
from django.db import models
from course.models import Course


class Document(models.Model):
    notes = models.TextField(blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d')
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return "{}:{}:{}".format(self.user, self.course_code, self.date)