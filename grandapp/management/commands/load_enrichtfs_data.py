from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Enrichtfs
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
        print("Loading disease data!")
        for row in DictReader(open('./data/cancerbio.csv')):
            disease = Enrichtfs()
            disease.term       = row['term']
            disease.go         = row['go']
            disease.logpval    = row['logpval']
            disease.cell       = row['cell']
            disease.save()
