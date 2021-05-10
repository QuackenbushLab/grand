from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Cancer
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
        print("Loading cancer data!")
        for row in DictReader(open('./data/cancer_aug.csv')):
            cancer = Cancer()
            cancer.tissue    = row['tissue']
            cancer.tcgacode  = row['tcgacode']
            cancer.cancer    = row['cancer']
            cancer.nnets     = row['nnets']
            cancer.datasets  = row['datasets']
            cancer.nnets2    = row['nnets2']
            cancer.nnetsref  = row['nnetsref']
            cancer.nnets2ref = row['nnets2ref']
            cancer.cancerref = row['cancerref']
            cancer.datasets2     = row['datasets2']
            cancer.datasetsref   = row['datasetsref']
            cancer.datasets2ref  = row['datasets2ref']
            cancer.types     = row['types']
            cancer.match     = row['tissuematch']
            cancer.ntfs      = row['ntfs'] 
            cancer.ngenes    = row['ngenes']
            cancer.nsamples  = row['nsamples']
            cancer.disp      = row['disp']
            cancer.dispname  = row['dispname']
            cancer.save()
