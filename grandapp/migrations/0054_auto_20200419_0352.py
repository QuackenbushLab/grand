# Generated by Django 3.0.5 on 2020-04-19 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0053_auto_20200419_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tissuesample',
            name='smatsscr',
            field=models.CharField(max_length=600),
        ),
    ]