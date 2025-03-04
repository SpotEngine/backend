# Generated by Django 5.1.3 on 2025-01-24 20:44

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perpetual', '0015_alter_position_pnl'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='liquidation_threshold',
            field=models.DecimalField(blank=True, decimal_places=6, default=Decimal('0.02'), max_digits=18, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))]),
        ),
        migrations.AlterField(
            model_name='position',
            name='status',
            field=models.CharField(blank=True, choices=[('open', 'open'), ('closed', 'closed'), ('liquidation', 'liquidation')], default='open', max_length=15, null=True),
        ),
    ]
