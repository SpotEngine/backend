# Generated by Django 5.1.3 on 2024-12-08 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perpetual', '0008_rename_close_only_order_reduce_only_alter_order_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='locked_size',
        ),
    ]
