# Generated by Django 3.0.2 on 2020-03-18 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0032_auto_20200318_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tissuelanding',
            name='netzooRel',
            field=models.CharField(max_length=200),
        ),
    ]
