# Generated by Django 3.2.5 on 2024-12-15 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0257_pancreassample_ss'),
    ]

    operations = [
        migrations.AddField(
            model_name='pancreassample',
            name='submitter_id_clean',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
