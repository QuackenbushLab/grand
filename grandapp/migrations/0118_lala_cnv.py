# Generated by Django 3.0.2 on 2021-03-22 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0117_auto_20210318_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='lala',
            name='cnv',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]