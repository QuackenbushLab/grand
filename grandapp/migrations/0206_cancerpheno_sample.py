# Generated by Django 3.0.2 on 2021-05-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0205_cancerpheno'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancerpheno',
            name='sample',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]