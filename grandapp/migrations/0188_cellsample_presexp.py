# Generated by Django 3.0.2 on 2021-04-25 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0187_tissueac'),
    ]

    operations = [
        migrations.AddField(
            model_name='cellsample',
            name='presexp',
            field=models.CharField(default=0, max_length=400),
            preserve_default=False,
        ),
    ]