from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Cellpage
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
    help = "Loads data from cell page into our model"

    def handle(self, *args, **options):
        print("Loading cell page data!")
        for row in DictReader(open('./data/cellspage.csv')):
            cell = Cellpage()
            cell.tissue   = row['tissue']
            cell.method   = row['method']
            cell.method2  = row['method2']
            cell.methodrefs2  = row['methodrefs2']
            cell.method3  = row['method3']
            cell.methodrefs3  = row['methodrefs3']
            cell.data     = row['data']
            cell.methodrefs   = row['methodrefs']
            cell.datarefs     = row['datarefs']
            cell.typenet   = row['type']
            cell.condition =  row['condition']
            cell.urllinks  =  row['urllinks']
            cell.reg       =  row['reg']
            cell.reg2      =  row['reg2']
            cell.save()
