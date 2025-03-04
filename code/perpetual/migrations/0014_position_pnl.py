# Generated by Django 5.1.3 on 2025-01-23 15:04

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perpetual', '0013_alter_position_leverage'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='pnl',
            field=models.DecimalField(blank=True, decimal_places=6, default=Decimal('0.0'), max_digits=18, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))]),
        ),
    ]
