# Generated by Django 5.1.3 on 2025-01-19 15:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aaa', '0001_initial'),
        ('spot', '0005_alter_order_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='aaa.account'),
        ),
    ]
