from django.db import models
from django.conf import settings


class Course(models.Model):
    course_title = models.TextField()
    course_code = models.CharField(max_length=6, unique=True)
    duration = models.IntegerField()
    #staff = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='staff')   # new
    course_info = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '{}:{}'.format(self.course_code, self.course_title)

