# Generated by Django 3.2.11 on 2022-06-10 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20220523_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(default='no_image.png', upload_to='images'),
        ),
    ]
