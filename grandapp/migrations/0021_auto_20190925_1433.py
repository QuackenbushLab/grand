# Generated by Django 2.1 on 2019-09-25 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0020_auto_20190925_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drugresultup',
            name='query',
        ),
        migrations.DeleteModel(
            name='Query',
        ),
    ]
