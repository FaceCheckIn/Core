# Generated by Django 5.0.4 on 2024-06-02 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facecheckin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='sentiment',
            field=models.CharField(blank=True, null=True, verbose_name='Sentiment'),
        ),
    ]
