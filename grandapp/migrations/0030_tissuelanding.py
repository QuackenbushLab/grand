# Generated by Django 3.0.2 on 2020-02-19 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0029_auto_20200219_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tissuelanding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tissue', models.CharField(max_length=200)),
                ('tissueLink', models.URLField(default='#')),
                ('tool', models.CharField(max_length=200)),
                ('netzoo', models.CharField(max_length=200)),
                ('netzooLink', models.URLField()),
                ('netzooRel', models.FloatField()),
                ('network', models.URLField()),
                ('ppi', models.URLField()),
                ('ppiLink', models.URLField()),
                ('motif', models.URLField()),
                ('expression', models.URLField()),
                ('expLink', models.URLField()),
                ('tfs', models.IntegerField()),
                ('genes', models.IntegerField()),
                ('refs', models.URLField()),
                ('refs2', models.URLField(default='#')),
                ('nnets', models.IntegerField(default=0)),
            ],
        ),
    ]