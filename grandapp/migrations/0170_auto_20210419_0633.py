# Generated by Django 3.0.2 on 2021-04-19 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0169_dragonac'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarmod',
            name='geneform',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarmod',
            name='goform',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarmod',
            name='gwasform',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarmod',
            name='tfform',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tarmod',
            name='tfgenesel',
            field=models.CharField(choices=[('nosel', 'nosel'), ('by gene', 'by gene'), ('by tf', 'by tf'), ('by GO', 'by GO'), ('by GWAS', 'by GWAS')], default='', max_length=200),
            preserve_default=False,
        ),
    ]
