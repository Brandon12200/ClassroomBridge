# Generated by Django 4.2.4 on 2024-01-13 03:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bridge', '0007_course_home_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='modules',
            field=models.ManyToManyField(blank=True, null=True, related_name='parent_classes', to='Bridge.module'),
        ),
        migrations.AlterField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='enrolled_classes', to=settings.AUTH_USER_MODEL),
        ),
    ]
