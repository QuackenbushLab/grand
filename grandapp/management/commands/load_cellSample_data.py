from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Cellsample
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
        print("Loading cell sample data!")
        for row in DictReader(open('./data/sample_info_aug2.csv')):
            drugsample = Cellsample()
            drugsample.depmap        = row['DepMap_ID']
            drugsample.stripcellname = row['stripped_cell_line_name']
            drugsample.cclename      = row['CCLE_Name']
            drugsample.cosmicid      = row['COSMICID']
            drugsample.sex           = row['sex']
            drugsample.source        = row['source']
            drugsample.culture       = row['culture_type']
            drugsample.cas9act       = row['cas9_activity']
            drugsample.collsite      = row['sample_collection_site']
            drugsample.prim          = row['primary_or_metastasis']
            drugsample.disease       = row['primary_disease']
            drugsample.subtype       = row['Subtype']
            drugsample.age           = row['age']
            drugsample.mutrate       = row['mutRate']
            drugsample.doublt        = row['doublt']
            drugsample.tcga          = row['tcga']
            drugsample.race          = row['race']
            drugsample.size          = row['size']
            drugsample.dummy         = row['dummy']
            drugsample.presexp       = row['presexp']
            drugsample.diffexp       = row['diffexp']
            drugsample.diffexpgenes  = row['diffexpgenes']
            drugsample.difftar       = row['difftar']
            drugsample.difftargenes  = row['difftargenes']
            drugsample.cleanname     = row['cleanname']
            drugsample.cleannamedis  = row['cleannamedis']
            drugsample.isdragon      = row['isdragon']
            drugsample.save()
