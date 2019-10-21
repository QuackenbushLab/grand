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
        for row in DictReader(open('./tissues.csv')):
            tissue = Tissue()
            tissue.tissue       = row['tissue']
            tissue.tissueLink   = row['tissueLink']
            tissue.tool         = row['tool']
            tissue.netzoo       = row['netzoo']
            tissue.netzooLink   = row['netzooLink']
            tissue.netzooRel    = row['netzooRel']
            tissue.network      = row['network']
            tissue.ppi          = row['ppi']
            tissue.ppiLink      = row['ppiLink']
            tissue.motif        = row['motif']
            tissue.expression   = row['expression']
            tissue.expLink      = row['expLink']
            tissue.tfs          = row['tfs']
            tissue.genes        = row['genes']
            tissue.refs         = row['refs']
            tissue.refs2        = row['refs2']
            tissue.save()
