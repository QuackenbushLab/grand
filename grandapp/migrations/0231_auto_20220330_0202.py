# Generated by Django 3.0.2 on 2022-03-30 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0230_celllanding_motifdesc'),
    ]

    operations = [
        migrations.AddField(
            model_name='celllanding',
            name='awsname',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='celllanding',
            name='tissue',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
