from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Drug
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
        print("Loading drug data!")
        for row in DictReader(open('./drugs.csv')):
            drug = Drug()
            drug.drug         = row['drug']
            drug.drugLink     = row['drugLink']
            drug.tool         = row['tool']
            drug.netzoo       = row['netzoo']
            drug.netzooLink   = row['netzooLink']
            drug.netzooRel    = row['netzooRel']
            drug.network      = row['network']
            drug.ppi          = row['ppi']
            drug.ppiLink      = row['ppiLink']
            drug.motif        = row['motif']
            drug.expression   = row['expression']
            drug.expLink      = row['expLink']
            drug.tfs          = row['tfs']
            drug.genes        = row['genes']
            drug.refs         = row['refs']
            drug.save()