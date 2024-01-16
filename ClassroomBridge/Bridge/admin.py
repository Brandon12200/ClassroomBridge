from django.contrib import admin
from .models import User, Module, Course

# Register your models here.
admin.site.register(User)
admin.site.register(Module)
admin.site.register(Course)