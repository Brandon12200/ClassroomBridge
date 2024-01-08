from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    id = models.AutoField(primary_key=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
