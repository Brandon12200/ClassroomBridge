from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    """
    pass

class Course(models.Model):
    """
    Course model representing a class in the system.
    """
    class_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taught_classes')
    location = models.CharField(max_length=100)
    class_picture = models.ImageField(upload_to='class_pictures/', null=True, blank=True)
    students = models.ManyToManyField(User, related_name='enrolled_classes', blank=True)
    modules = models.ManyToManyField('Module', related_name='parent_classes', blank=True)
    home_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.class_name

class Module(models.Model):
    """
    Module model representing educational content within courses.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self):
        return self.title