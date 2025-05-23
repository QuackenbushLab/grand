from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Cancerpheno
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
        print("Loading cancer geo sample data!")
        for row in DictReader(open('./data/cancerpheno_extended.csv')):
            geosample = Cancerpheno()
            geosample.sample               = row['sample']
            geosample.gender               = row['gender']
            geosample.race                 = row['race']
            geosample.ajcc                 = row['ajcc_pathologic_tumor_stage']
            geosample.vital_status         = row['vital_status']
            geosample.age                  = row['age_at_initial_pathologic_diagnosis']
            geosample.days_to_last_followup= row['days_to_last_followup']
            geosample.tumorID              = row['tumorID']
            geosample.link              = row['link']
            geosample.size              = row['size']
            geosample.ss                = row['ss']
            geosample.submitter_id_clean= row['submitter_id_clean']
            geosample.save()
