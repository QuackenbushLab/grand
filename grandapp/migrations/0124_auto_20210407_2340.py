# Generated by Django 3.0.2 on 2021-04-07 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0123_netmod_absval'),
    ]

    operations = [
        migrations.AddField(
            model_name='netmod',
            name='genesel',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='netmod',
            name='tfsel',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
