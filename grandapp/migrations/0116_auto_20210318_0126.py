# Generated by Django 3.0.2 on 2021-03-18 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0115_lala_absval'),
    ]

    operations = [
        migrations.AddField(
            model_name='lala',
            name='connex',
            field=models.CharField(choices=[('Largest', 'Largest'), ('Smallest', 'Smallest')], default='Methylation', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lala',
            name='gp',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]