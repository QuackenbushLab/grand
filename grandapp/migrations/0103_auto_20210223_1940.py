# Generated by Django 3.0.2 on 2021-02-23 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0102_ggbmd1sample'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ggbmd2sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitter_id', models.CharField(max_length=200)),
                ('yearstobirth', models.CharField(max_length=200)),
                ('vitalstatus', models.CharField(max_length=200)),
                ('daystodeath', models.CharField(max_length=200)),
                ('daystolastfollowup', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=200)),
                ('dateofinitialpathologicdiagnosis', models.CharField(max_length=200)),
                ('radiationtherapy', models.CharField(max_length=200)),
                ('karnofskyperformancescore', models.CharField(max_length=200)),
                ('histologicaltype', models.CharField(max_length=200)),
                ('radiationsradiationregimenindication', models.CharField(max_length=200)),
                ('race', models.CharField(max_length=200)),
                ('ethnicitity', models.CharField(max_length=200)),
                ('neoadjuvanttherapy', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='cancer',
            name='subtype',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]