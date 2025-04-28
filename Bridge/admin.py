from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Module, Course

class CourseAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'teacher', 'location', 'created_at')
    list_filter = ('teacher', 'created_at')
    search_fields = ('class_name', 'teacher__username', 'location')
    filter_horizontal = ('students', 'modules')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('class_name', 'teacher', 'location')
        }),
        ('Content', {
            'fields': ('class_picture', 'home_content')
        }),
        ('Relationships', {
            'fields': ('students', 'modules')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'order')
        }),
        ('Content', {
            'fields': ('description', 'content')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

# Register models with custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Course, CourseAdmin)