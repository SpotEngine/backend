# Generated by Django 5.1.3 on 2024-11-29 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('aaa', '0001_initial'),
        ('spot', '0001_initial'),
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='token',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spot_income', to='wallet.token'),
        ),
        migrations.AddField(
            model_name='order',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='spot_order', to='aaa.account'),
        ),
        migrations.AddField(
            model_name='order',
            name='locked_asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wallet.asset'),
        ),
        migrations.AddField(
            model_name='symbol',
            name='base',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='base', to='wallet.token'),
        ),
        migrations.AddField(
            model_name='symbol',
            name='quote',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='quote', to='wallet.token'),
        ),
        migrations.AddField(
            model_name='order',
            name='symbol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='spot.symbol'),
        ),
        migrations.AddField(
            model_name='trade',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='spot.order'),
        ),
        migrations.AddField(
            model_name='trade',
            name='paid_token',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='paid', to='wallet.token'),
        ),
        migrations.AddField(
            model_name='trade',
            name='received_token',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='received', to='wallet.token'),
        ),
        migrations.AddField(
            model_name='trade',
            name='symbol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='spot.symbol'),
        ),
        migrations.AddField(
            model_name='income',
            name='trade',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spot.trade'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['side', 'price'], name='spot_order_side_2c1232_idx'),
        ),
    ]
