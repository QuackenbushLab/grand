# Generated by Django 3.0.2 on 2021-02-24 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0104_auto_20210224_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='ggbmd1sample',
            name='link',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ggbmd1sample',
            name='size',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ggbmd2sample',
            name='link',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ggbmd2sample',
            name='size',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
