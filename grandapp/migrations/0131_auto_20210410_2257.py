# Generated by Django 3.0.2 on 2021-04-10 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0130_auto_20210410_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugcombsdown',
            name='query',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='drugcombsup',
            name='query',
            field=models.IntegerField(default=0),
        ),
    ]