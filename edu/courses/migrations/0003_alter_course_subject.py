# Generated by Django 3.2.11 on 2022-03-26 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20220325_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.subject'),
        ),
    ]
