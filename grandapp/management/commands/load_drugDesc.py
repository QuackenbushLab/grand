from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Drugdesc
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
        print("Loading drug description data!")
        for row in DictReader(open('./data/drug_desc.csv')):
            drugdesc = Drugdesc()
            drugdesc.expected_mass = row['expected_mass']
            drugdesc.smiles        = row['smiles']
            drugdesc.InChIKey      = row['InChIKey']
            drugdesc.pubchem_cid   = row['pubchem_cid']
            drugdesc.pert_iname     = row['pert_iname']
            drugdesc.clinical_phase = row['clinical_phase']
            drugdesc.moa            = row['moa']
            drugdesc.target         = row['target']
            drugdesc.disease_area   = row['disease_area']
            drugdesc.indication     = row['indication']
            drugdesc.broad_id       = row['broad_id']
            drugdesc.save()
