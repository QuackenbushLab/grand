# Generated by Django 3.0.2 on 2020-03-21 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0034_auto_20200320_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='cell',
            name='samples',
            field=models.IntegerField(default=0),
        ),
    ]