# Generated by Django 5.1.3 on 2025-02-19 14:59

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0007_alter_symbol_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='fee_rebate',
            field=models.DecimalField(blank=True, decimal_places=6, default=Decimal('0.0'), max_digits=18, null=True),
        ),
    ]
