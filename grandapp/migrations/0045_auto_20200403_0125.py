# Generated by Django 3.0.2 on 2020-04-03 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0044_auto_20200403_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugresultdown',
            name='druglink',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultup',
            name='druglink',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
