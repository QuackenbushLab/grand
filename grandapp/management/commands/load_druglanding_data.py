from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Druglanding
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
        print("Loading drug landing data!")
        for row in DictReader(open('./drugslanding.csv')):
            drugslanding = Druglanding()
            drugslanding.number       = row['number']
            drugslanding.drug         = row['drug']
            drugslanding.tool         = row['tool']
            drugslanding.netzoo       = row['netzoo']
            drugslanding.netzooRel    = row['netzooRel'] 
            drugslanding.network      = row['network']
            drugslanding.ppi          = row['ppi']
            drugslanding.motif        = row['motif']
            drugslanding.expression   = row['expression']
            drugslanding.tfs          = row['tfs']
            drugslanding.genes        = row['genes']
            drugslanding.refs         = row['refs']
            drugslanding.ppiLink      = row['ppiLink']
            drugslanding.samples      = row['samples']
            drugslanding.expLink      = row['expLink']
            drugslanding.save()
