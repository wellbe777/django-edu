# Generated by Django 3.2.11 on 2022-07-03 10:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0011_studentcourses'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='courses_joined', through='courses.StudentCourses', to=settings.AUTH_USER_MODEL),
        ),
    ]
