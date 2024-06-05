# Generated by Django 5.0.4 on 2024-06-05 10:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facecheckin', '0002_alter_transaction_sentiment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='datetime',
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created_at'),
            preserve_default=False,
        ),
    ]
