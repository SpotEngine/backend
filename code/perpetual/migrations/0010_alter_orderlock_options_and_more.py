# Generated by Django 5.1.3 on 2024-12-08 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aaa', '0001_initial'),
        ('perpetual', '0009_remove_position_locked_size'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderlock',
            options={},
        ),
        migrations.AddIndex(
            model_name='orderlock',
            index=models.Index(fields=['position'], name='perpetual_o_positio_655f2f_idx'),
        ),
    ]
