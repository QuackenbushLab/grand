# Generated by Django 3.0.2 on 2021-02-19 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grandapp', '0096_tissuelanding_refs3'),
    ]

    operations = [
        migrations.AddField(
            model_name='drugresultdown',
            name='altid',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultdown',
            name='canonical_smiles',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultdown',
            name='inchi_key',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultdown',
            name='inchi_key_prefix',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultdown',
            name='pubchem_cid',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultup',
            name='altid',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultup',
            name='canonical_smiles',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultup',
            name='inchi_key',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultup',
            name='inchi_key_prefix',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='drugresultup',
            name='pubchem_cid',
            field=models.CharField(default='', max_length=400),
            preserve_default=False,
        ),
    ]