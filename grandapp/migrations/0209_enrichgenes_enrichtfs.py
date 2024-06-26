# Generated by Django 3.0.2 on 2021-05-09 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0208_cellsample_isdragon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrichgenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell', models.CharField(max_length=600)),
                ('term', models.CharField(max_length=600)),
                ('go', models.CharField(max_length=600)),
                ('logpval', models.CharField(max_length=600)),
            ],
        ),
        migrations.CreateModel(
            name='Enrichtfs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cell', models.CharField(max_length=600)),
                ('term', models.CharField(max_length=600)),
                ('go', models.CharField(max_length=600)),
                ('logpval', models.CharField(max_length=600)),
            ],
        ),
    ]
