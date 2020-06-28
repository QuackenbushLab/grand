from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Tcgasample
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
        print("Loading cancer sample data!")
        for row in DictReader(open('./data/clinical_tcga.csv')):
            tcgasample = Tcgasample()
            tcgasample.sample     = row['sample']
            tcgasample.platform   = row['Platform']
            tcgasample.gender     = row['gender']
            tcgasample.race       = row['race']
            tcgasample.weight_kg_at_diagnosis     = row['weight_kg_at_diagnosis']
            tcgasample.height_cm_at_diagnosis     = row['height_cm_at_diagnosis']
            tcgasample.age_at_initial_pathologic_diagnosis = row['age_at_initial_pathologic_diagnosis']
            tcgasample.anatomic_neoplasm_subdivision       = row['anatomic_neoplasm_subdivision']
            tcgasample.uicc_stage      = row['uicc_stage']
            tcgasample.time_to_event   = row['time_to_event']
            tcgasample.vital_status    = row['vital_status'] 
            tcgasample.size    = row['size']
            tcgasample.link    = row['link']
            tcgasample.save()
