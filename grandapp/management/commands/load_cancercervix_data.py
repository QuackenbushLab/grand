from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Cervixsample
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
        print("Loading cancer cervix sample data!")
        for row in DictReader(open('./data/metadata_cervix_07202020.csv')):
            breastsample = Cervixsample()
            breastsample.sample = row['gdc_cases.samples.portions.analytes.aliquots.submitter_id']
            breastsample.gender = row['gdc_cases.demographic.gender']
            breastsample.race = row['gdc_cases.demographic.race']
            breastsample.ethnicity = row['gdc_cases.demographic.ethnicity']
            breastsample.weight_kg_at_diagnosis = row['gdc_cases.exposures.weight']
            breastsample.height_cm_at_diagnosis = row['gdc_cases.exposures.height']
            breastsample.primary_site = row['gdc_cases.project.primary_site']
            breastsample.primary_diagnosis=row['gdc_cases.diagnoses.primary_diagnosis']
            breastsample.age_at_initial_pathologic_diagnosis = row['cgc_case_age_at_diagnosis']
            breastsample.uicc_stage = row['gdc_cases.diagnoses.tumor_stage']
            breastsample.time_to_event = row['gdc_cases.diagnoses.days_to_death']
            breastsample.vital_status = row['gdc_cases.diagnoses.vital_status']
            breastsample.save()
