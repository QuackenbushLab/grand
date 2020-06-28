from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Geosample
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
        for row in DictReader(open('./data/clinical_geo.csv')):
            geosample = Geosample()
            geosample.sample     = row['sample']
            geosample.gender     = row['gender']
            geosample.race       = row['race']
            geosample.age_at_initial_pathologic_diagnosis = row['age_at_initial_pathologic_diagnosis']
            geosample.tumor_location  = row['tumor_location']
            geosample.uicc_stage      = row['uicc_stage']
            geosample.time_to_event   = row['time_to_event']
            geosample.vital_status    = row['vital_status']
            geosample.geoid           = row['geoID'] 
            geosample.size           = row['size']
            geosample.link           = row['link']
            geosample.save()
