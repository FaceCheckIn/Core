# Generated by Django 5.0.4 on 2024-04-22 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='identification_code',
            field=models.CharField(default=None, unique=True, verbose_name='Identification Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='image1',
            field=models.ImageField(null=True, upload_to='user/', verbose_name='Image1'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='image2',
            field=models.ImageField(null=True, upload_to='user/', verbose_name='Image2'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(default=None, verbose_name='Role'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]