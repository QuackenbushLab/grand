# Generated by Django 3.0.5 on 2020-04-26 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0063_auto_20200426_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugresultdown',
            name='idd',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='drugresultdown',
            name='nuser',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='drugresultup',
            name='idd',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='drugresultup',
            name='nuser',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='drugresultdown',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='drugresultup',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
