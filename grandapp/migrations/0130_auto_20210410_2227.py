# Generated by Django 3.0.2 on 2021-04-10 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0129_drugcombsdown_drugcombsup'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugcombsdown',
            name='idd',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='drugcombsdown',
            name='nuser',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='drugcombsup',
            name='idd',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='drugcombsup',
            name='nuser',
            field=models.IntegerField(default=0),
        ),
    ]
