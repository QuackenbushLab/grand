# Generated by Django 3.0.2 on 2021-05-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0203_auto_20210503_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancerlanding',
            name='tcgacode',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]