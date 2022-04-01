from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Egret
from pytz import UTC


DATETIME_FORMAT = '%m/%d/%Y %H:%M'

VACCINES_NAMES = [
    'Canine Parvo',
    'Canine Distemper',
    'Canine Rabies',
    'Canine Leptospira',
    'Feline Herpes Virus 1',
    'Feline Rabies',
    'Feline Leukemia'
]

ALREADY_LOADED_ERROR_MESSAGE = """
If you need to reload the pet data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from pet_data.csv into our Pet model"

    def handle(self, *args, **options):
        print("Loading EGRET data!")
        for row in DictReader(open('./data/diffexp_banovich_YRI_genotype_info_for_grand.csv')):
            egret = Egret()
            egret.sample    = row['Sample.name']
            egret.sex       = row['Sex']
            egret.idd       = row['Biosample.ID']
            egret.code      = row['Population.code']
            egret.name      = row['Population.name']
            egret.supcode   = row['Superpopulation.code']
            egret.supname   = row['Superpopulation.name']
            egret.iid       = row['Population.elastic.ID']
            egret.datac     = row['Data.collections']
            egret.size1       = row['size1']
            egret.cleanname1  = row['cleanname1']
            egret.net         = row['net']
            egret.reflink     = row['reflink']
            egret.diffexp       = row['diffexp']
            egret.diffexpgenes  = row['diffexpgenes']
            egret.difftar       = row['difftar']
            egret.difftargenes  = row['difftargenes']
            egret.presexp       = row['presexp']
            egret.save()
