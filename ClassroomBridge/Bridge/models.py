from django.db import models
from django.contrib.auth.models import AbstractUser, User

class User(AbstractUser):
    pass

class Course(models.Model):
    class_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_classes')
    location = models.CharField(max_length=100)
    class_picture = models.URLField(max_length=200000, null=True, blank=True)
    students = models.ManyToManyField(User, related_name='enrolled_classes', blank=True)
    modules = models.ManyToManyField('Module', related_name='parent_classes', blank=True)
    home_content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.class_name

class Module(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.title