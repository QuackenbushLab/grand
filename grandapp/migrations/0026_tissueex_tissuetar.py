# Generated by Django 2.1 on 2019-10-21 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0025_tissue_refs2'),
    ]

    operations = [
        migrations.CreateModel(
            name='TissueEx',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tissue', models.CharField(max_length=600)),
                ('count', models.IntegerField()),
                ('intersect', models.IntegerField()),
                ('pval', models.FloatField()),
                ('qval', models.FloatField()),
                ('query', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TissueTar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tissue', models.CharField(max_length=600)),
                ('count', models.IntegerField()),
                ('intersect', models.IntegerField()),
                ('pval', models.FloatField()),
                ('qval', models.FloatField()),
                ('query', models.IntegerField(default=0)),
            ],
        ),
    ]
