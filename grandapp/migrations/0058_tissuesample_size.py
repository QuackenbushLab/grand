# Generated by Django 3.0.5 on 2020-04-19 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0057_tissuesample_grdid'),
    ]

    operations = [
        migrations.AddField(
            model_name='tissuesample',
            name='size',
            field=models.CharField(default='', max_length=600),
            preserve_default=False,
        ),
    ]
