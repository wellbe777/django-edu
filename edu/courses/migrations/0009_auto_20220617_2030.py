# Generated by Django 3.2.11 on 2022-06-17 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='course',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
