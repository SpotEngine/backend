# Generated by Django 5.1.3 on 2024-12-07 17:34

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aaa', '0001_initial'),
        ('perpetual', '0005_trade_match_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderLock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=6, default=Decimal('0.0'), max_digits=18, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))])),
                ('size', models.DecimalField(blank=True, decimal_places=6, default=Decimal('0.0'), max_digits=18, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))])),
                ('fee', models.DecimalField(blank=True, decimal_places=6, default=Decimal('0.0'), max_digits=18, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))])),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='position',
            options={},
        ),
        migrations.AddField(
            model_name='position',
            name='locked_size',
            field=models.DecimalField(blank=True, decimal_places=6, default=Decimal('0.0'), max_digits=18, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))]),
        ),
        migrations.AddIndex(
            model_name='position',
            index=models.Index(fields=['contract', 'status'], name='perpetual_p_contrac_fa8416_idx'),
        ),
        migrations.AddField(
            model_name='orderlock',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='perp_orderlock', to='aaa.account'),
        ),
        migrations.AddField(
            model_name='orderlock',
            name='asset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='perpetual.perpetualwallet'),
        ),
        migrations.AddField(
            model_name='orderlock',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='perpetual.position'),
        ),
        migrations.AddField(
            model_name='order',
            name='locked',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='perpetual.orderlock'),
        ),
    ]
