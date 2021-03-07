from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Pancreassample
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
        print("Loading pancreas tcga sample data!")
        for row in DictReader(open('./static/data/pancreas_tcga.csv')):
            pancreassample = Pancreassample()
            pancreassample.sample     = row['gdc_cases.samples.portions.analytes.aliquots.submitter_id']
            pancreassample.gender     = row['gdc_cases.demographic.gender']
            pancreassample.race       = row['gdc_cases.demographic.race']
            pancreassample.primary_site = row['gdc_cases.project.primary_site']
            pancreassample.primary_diagnosis       = row['gdc_cases.diagnoses.primary_diagnosis']
            pancreassample.age_at_initial_pathologic_diagnosis      = row['cgc_case_age_at_diagnosis']
            pancreassample.uicc_stage   = row['gdc_cases.diagnoses.tumor_stage']
            pancreassample.time_to_event= row['gdc_cases.diagnoses.days_to_death'] 
            pancreassample.size    = row['size']
            pancreassample.link    = row['link']
            pancreassample.ethnicity = row['gdc_cases.demographic.ethnicity']
            pancreassample.vital_status = row['gdc_cases.diagnoses.vital_status']
            pancreassample.subtype = row['subtype']
            pancreassample.save()
