# Generated by Django 3.0.2 on 2020-03-20 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0033_auto_20200318_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drug',
            name='expression',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='genes',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='motif',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='network',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='netzoo',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='ppi',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='refs',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='tfs',
        ),
        migrations.RemoveField(
            model_name='drug',
            name='tool',
        ),
        migrations.AddField(
            model_name='drug',
            name='nnets',
            field=models.IntegerField(default='0'),
        ),
    ]
