# Generated by Django 3.0.2 on 2021-05-03 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0202_auto_20210503_0537'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancer',
            name='disp',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cancer',
            name='dispname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]