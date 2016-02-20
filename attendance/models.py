from django.db import models
from django.conf import settings
import time


class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user')
    course_code = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    timestamp = models.FloatField(default=time.time())

    class Meta:
        unique_together = ('user', 'course_code', 'date',)

    def __unicode__(self):
        return "{}:{}:{}".format(self.user, self.course_code, self.date)


#datetime.utcfromtimestamp(time.time()) to convert timestamp to utc time. Localtime is 1h ahead