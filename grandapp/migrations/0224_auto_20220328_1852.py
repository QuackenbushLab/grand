# Generated by Django 3.0.2 on 2022-03-28 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0223_remove_celllanding_cancerlink'),
    ]

    operations = [
        migrations.RenameField(
            model_name='egret',
            old_name='size',
            new_name='size1',
        ),
    ]