# Generated by Django 5.1.3 on 2024-12-07 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perpetual', '0006_orderlock_alter_position_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='locked_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='locked_asset',
        ),
        migrations.RemoveField(
            model_name='order',
            name='locked_fee',
        ),
    ]
