# Generated by Django 3.0.2 on 2022-03-29 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0227_egret_reflink'),
    ]

    operations = [
        migrations.AddField(
            model_name='cellpage',
            name='method3',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cellpage',
            name='methodrefs3',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
    ]