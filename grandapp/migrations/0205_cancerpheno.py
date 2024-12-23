# Generated by Django 3.0.2 on 2021-05-04 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0204_cancerlanding_tcgacode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cancerpheno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=200)),
                ('race', models.CharField(max_length=200)),
                ('ajcc_pathologic_tumor_stage', models.CharField(max_length=200)),
                ('vital_status', models.CharField(max_length=200)),
                ('age_at_initial_pathologic_diagnosis', models.CharField(max_length=200)),
                ('days_to_last_followup', models.CharField(max_length=200)),
                ('tumorID', models.CharField(max_length=200)),
            ],
        ),
    ]
