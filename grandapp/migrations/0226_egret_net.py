# Generated by Django 3.0.2 on 2022-03-29 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0225_egret_cleanname1'),
    ]

    operations = [
        migrations.AddField(
            model_name='egret',
            name='net',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]