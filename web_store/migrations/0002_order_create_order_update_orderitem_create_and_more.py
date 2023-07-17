# Generated by Django 4.2.1 on 2023-06-05 14:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='update',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='update',
            field=models.DateField(auto_now=True),
        ),
    ]