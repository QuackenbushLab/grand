# Generated by Django 3.0.5 on 2020-05-27 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0080_drugdesc_broad_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugsample',
            name='infl',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
