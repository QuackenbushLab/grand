# Generated by Django 3.2.5 on 2024-12-15 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0256_auto_20241215_0530'),
    ]

    operations = [
        migrations.AddField(
            model_name='pancreassample',
            name='ss',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]