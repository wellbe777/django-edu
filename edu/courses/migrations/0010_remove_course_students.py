# Generated by Django 3.2.11 on 2022-07-03 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_auto_20220617_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='students',
        ),
    ]
