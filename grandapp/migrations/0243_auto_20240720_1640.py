# Generated by Django 3.2.5 on 2024-07-20 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0242_auto_20240719_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='gse197sample',
            name='link',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gse197sample',
            name='size',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
