# Generated by Django 3.0.2 on 2020-02-19 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0030_tissuelanding'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tissue',
            name='expLink',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='expression',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='genes',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='motif',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='network',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='netzoo',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='netzooLink',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='netzooRel',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='ppi',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='ppiLink',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='refs',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='refs2',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='tfs',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='tissueLink',
        ),
        migrations.RemoveField(
            model_name='tissue',
            name='tool',
        ),
    ]
