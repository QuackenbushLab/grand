# Generated by Django 2.1 on 2019-10-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0026_tissueex_tissuetar'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrugApi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default='0')),
                ('drug', models.CharField(max_length=400)),
                ('tool', models.CharField(max_length=400)),
                ('netzoo', models.CharField(max_length=400)),
                ('network', models.CharField(max_length=400)),
                ('ppi', models.CharField(max_length=400)),
                ('motif', models.CharField(max_length=400)),
                ('expression', models.CharField(max_length=400)),
                ('tfs', models.IntegerField()),
                ('genes', models.IntegerField()),
                ('refs', models.CharField(max_length=400)),
            ],
        ),
    ]