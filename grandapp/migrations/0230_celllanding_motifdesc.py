# Generated by Django 3.0.2 on 2022-03-30 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0229_auto_20220329_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='celllanding',
            name='motifDesc',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
