# Generated by Django 3.0.2 on 2021-04-07 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0124_auto_20210407_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='netmod',
            name='geneform',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='netmod',
            name='tfform',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]