# Generated by Django 3.0.2 on 2021-04-23 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0179_auto_20210422_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='tissuesample',
            name='smmncpb',
            field=models.CharField(default='', max_length=600),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tissuesample',
            name='smrdlgth',
            field=models.CharField(default='', max_length=600),
            preserve_default=False,
        ),
    ]
