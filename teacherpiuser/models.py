from django.db import models
from django.contrib.auth.models import AbstractUser


class TeacherPiUser(AbstractUser):
    identity = models.CharField(max_length=14, unique=True)


class DefaultPass(models.Model):
    password = models.CharField(max_length=20, unique=True, default='pass.electno')


class MacAddress(models.Model):
    owner = models.ForeignKey(TeacherPiUser, related_name='mac_addresses')
    mac_add = models.CharField(max_length=17, null=True, blank=True, unique=True)