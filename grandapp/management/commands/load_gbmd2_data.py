from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Ggbmd2sample
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
        print("Loading gbm d2 data!")
        for row in DictReader(open('./static/data/GBM_d2_clinvar.csv')):
            gbmd2sample = Ggbmd2sample()
            gbmd2sample.submitter_id        = row['submitter_id']
            gbmd2sample.yearstobirth        = row['yearstobirth']
            gbmd2sample.vitalstatus         = row['vitalstatus']
            gbmd2sample.daystodeath         = row['daystodeath']
            gbmd2sample.daystolastfollowup  = row['daystolastfollowup']
            gbmd2sample.gender              = row['gender']
            gbmd2sample.dateofinitialpathologicdiagnosis  = row['dateofinitialpathologicdiagnosis']
            gbmd2sample.radiationtherapy    = row['radiationtherapy']
            gbmd2sample.karnofskyperformancescore        = row['karnofskyperformancescore']
            gbmd2sample.histologicaltype    = row['histologicaltype']
            gbmd2sample.radiationsradiationregimenindication= row['radiationsradiationregimenindication']
            gbmd2sample.race                = row['race']
            gbmd2sample.ethnicity         = row['ethnicity']
            gbmd2sample.neoadjuvanttherapy  = row['neoadjuvanttherapy']
            gbmd2sample.size                = row['size']
            gbmd2sample.link                = row['link']
            gbmd2sample.platform            = row['platform']
            gbmd2sample.save()
