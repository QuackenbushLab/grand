# Generated by Django 3.0.2 on 2021-04-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0192_cellsample_difftargenes'),
    ]

    operations = [
        migrations.AddField(
            model_name='netmod',
            name='edgetargeting',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]