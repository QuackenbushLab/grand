# Generated by Django 2.1 on 2019-09-18 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0012_auto_20190917_0212'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrugResultDown',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('drug', models.CharField(max_length=400)),
                ('overlap', models.FloatField()),
                ('cosine', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DrugResultUp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('drug', models.CharField(max_length=400)),
                ('overlap', models.FloatField()),
                ('cosine', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='DrugResult',
        ),
    ]