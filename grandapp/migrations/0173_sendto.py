# Generated by Django 3.0.2 on 2021-04-20 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0172_auto_20210420_0159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sendto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preload', models.IntegerField(default=0)),
                ('idd', models.IntegerField(default=0)),
            ],
        ),
    ]