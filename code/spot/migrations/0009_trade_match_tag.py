# Generated by Django 5.1.3 on 2025-02-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0008_order_fee_rebate'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='match_tag',
            field=models.CharField(blank=True, default='', max_length=40, null=True),
        ),
    ]
