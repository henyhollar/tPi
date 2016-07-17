from django.db import models
from course.models import Course
from jsonfield import JSONField
from teacherpiuser.models import TeacherPiUser

QUESTION_CHOICES = (
    (0, "Fill in the gap"),
    (1, "Single-choice"),
    (2, "Multi-choice")
)


class Questions(models.Manager):
    course = models.ForeignKey(Course)
    topic = models.CharField(max_length=300, unique=True)
    question = JSONField(unique=True)
    question_type = models.IntegerField(choices=QUESTION_CHOICES, default=1)
    answers = JSONField(null=True)


class Results(models.Model):
    user = models.ForeignKey(TeacherPiUser)
    question = models.ForeignKey(Questions)
    submission = JSONField()  # store a list of dictionaries
    mark_obtained = models.IntegerField(blank=True)  # cook a function to obtain the mark from submitted answers
    date = models.DateField(auto_now=True)
