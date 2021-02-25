from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Cancerlanding
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
        print("Loading cancer landing data!")
        for row in DictReader(open('./data/cancerlanding.csv')):
            tissuelanding = Cancerlanding()
            tissuelanding.cancer       = row['cancer']
            tissuelanding.cancerLink   = row['cancerLink']
            tissuelanding.tool         = row['tool']
            tissuelanding.netzoo       = row['netzoo']
            tissuelanding.netzooLink   = row['netzooLink']
            tissuelanding.netzooRel    = row['netzooRel']
            tissuelanding.network      = row['network']
            tissuelanding.ppi          = row['ppi']
            tissuelanding.ppiLink      = row['ppiLink']
            tissuelanding.motif        = row['motif']
            tissuelanding.expression   = row['expression']
            tissuelanding.expLink      = row['expLink']
            tissuelanding.tfs          = row['tfs']
            tissuelanding.genes        = row['genes']
            tissuelanding.refs         = row['refs']
            tissuelanding.refs2        = row['refs2']
            tissuelanding.samples      = row['samples']
            tissuelanding.cardref      = row['cardref']
            tissuelanding.script       = row['script']
            tissuelanding.dataset       = row['dataset']
            tissuelanding.save()
