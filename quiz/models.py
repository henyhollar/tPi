from django.db import models
from course.models import Course
from jsonfield import JSONField


class Questions(models.Manager):
    def ordered_questions(self):
        pass    # give random order to each returned list of questions. Include the id of each question


class Topic(models.Model):
    course = models.ForeignKey(Course)
    topic = models.CharField(max_length=200, unique=True)


class Question(models.Model):
    topic = models.ForeignKey(Topic)
    question = models.TextField(unique=True)
    answer = models.TextField(blank=True, null=True)


class Submission(models.Model):
    submission = JSONField()
    statistics = JSONField()