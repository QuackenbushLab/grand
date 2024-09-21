from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Tissuesamplethy
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
        print("Loading tissue sample data for BONOBO thyroid networks!")
        for row in DictReader(open('./static/data/GTEx_thyroid_phenotypes_GRAND_red.csv')):
            tissuesamplethy = Tissuesamplethy()
            tissuesamplethy.sampleid    = row['id']
            tissuesamplethy.subjectid   = row['gtex_subjid']
            tissuesamplethy.gender      = row['gtex_sex']
            tissuesamplethy.age         = row['gtex_age']
            tissuesamplethy.dthhrdy     = row['gtex_dthhrdy']
            tissuesamplethy.smatsscr    = row['gtex_smatsscr']
            tissuesamplethy.smrin       = row['gtex_smrin']
            tissuesamplethy.smts        = row['gtex_smts']
            tissuesamplethy.smubrid     = row['gtex_smubrid'] 
            tissuesamplethy.smtsisch    = row['gtex_smtsisch']
            tissuesamplethy.proxage     = row['proxy_continuous_age']
            tissuesamplethy.link        = row['link']
            tissuesamplethy.size        = row['size']
            tissuesamplethy.cleanname   = row['cleanname']
            tissuesamplethy.decsex      = row['decoded_sex']
            tissuesamplethy.save()
