from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Tissuesample
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
        print("Loading tissue sample data!")
        for row in DictReader(open('./data/GTExSamples_Variables.csv')):
            tissuesample = Tissuesample()
            tissuesample.sampleid    = row['SampleID']
            tissuesample.subjectid   = row['SubjectID']
            tissuesample.tissueid    = row['TissueID']
            tissuesample.gender      = row['GENDER']
            tissuesample.age         = row['AGE']
            tissuesample.dthhrdy     = row['DTHHRDY']
            tissuesample.smatsscr    = row['SMATSSCR']
            tissuesample.smrin       = row['SMRIN']
            tissuesample.smts        = row['SMTS']
            tissuesample.smtsd       = row['SMTSD']
            tissuesample.smubrid     = row['SMUBRID'] 
            tissuesample.smtsisch    = row['SMTSISCH']
            tissuesample.grdid       = row['grdID']
            tissuesample.size        = row['size']
            tissuesample.link        = row['link']
            tissuesample.smtstptref  = row['SMTSTPTREF']
            tissuesample.save()
