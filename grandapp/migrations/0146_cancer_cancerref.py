# Generated by Django 3.0.2 on 2021-04-15 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0145_cellpage_urllinks'),
    ]

    operations = [
        migrations.AddField(
            model_name='cancer',
            name='cancerref',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]