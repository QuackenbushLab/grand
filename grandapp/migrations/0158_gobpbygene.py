# Generated by Django 3.0.2 on 2021-04-17 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0157_auto_20210416_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gobpbygene',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gene', models.CharField(max_length=400)),
                ('termlist', models.CharField(max_length=3000)),
            ],
        ),
    ]