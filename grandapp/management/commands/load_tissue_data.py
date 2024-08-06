from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Tissue
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
        print("Loading tissue data!")
        for row in DictReader(open('./data/tissues.csv')):
            tissue = Tissue()
            tissue.tissue    = row['tissue']
            tissue.nnets     = row['nnets']
            tissue.tool1     = row['tool1']   
            tissue.tool2     = row['tool2']   
            tissue.tool3     = row['tool3']   
            tissue.tool4     = row['tool4']   
            tissue.nettype   = row['nettype']
            tissue.reg       = row['reg']
            tissue.tissuename= row['tissuename']
            tissue.reftool1  = row['reftool1']
            tissue.reftool2  = row['reftool2']
            tissue.reftool3  = row['reftool3']
            tissue.reftool4  = row['reftool4']
            tissue.nsamples  = row['nsamples']
            tissue.save()
