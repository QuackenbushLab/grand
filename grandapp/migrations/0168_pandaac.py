# Generated by Django 3.0.2 on 2021-04-18 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0167_otterac_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pandaac',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ko', models.FloatField()),
                ('cc', models.FloatField()),
                ('sr', models.FloatField()),
                ('method', models.CharField(max_length=200)),
            ],
        ),
    ]
