# Generated by Django 3.0.2 on 2022-07-25 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0237_tissuesampleegret'),
    ]

    operations = [
        migrations.AddField(
            model_name='tissuesampleegret',
            name='cleanname',
            field=models.CharField(default='', max_length=600),
            preserve_default=False,
        ),
    ]