# Generated by Django 3.0.2 on 2020-04-04 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0046_auto_20200404_0206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gwas',
            name='query',
        ),
        migrations.RemoveField(
            model_name='tissueex',
            name='query',
        ),
        migrations.RemoveField(
            model_name='tissuetar',
            name='query',
        ),
        migrations.AddField(
            model_name='tissueex',
            name='tissueLink',
            field=models.URLField(default='', verbose_name='#'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tissuetar',
            name='tissueLink',
            field=models.URLField(default='', verbose_name='#'),
            preserve_default=False,
        ),
    ]