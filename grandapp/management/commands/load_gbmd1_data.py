from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Ggbmd1sample
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
        print("Loading gbm d1 data!")
        for row in DictReader(open('./static/data/GBM_d1_clinvar.csv')):
            gbmd1sample = Ggbmd1sample()
            gbmd1sample.submitter_id        = row['submitter_id']
            gbmd1sample.yearstobirth        = row['yearstobirth']
            gbmd1sample.vitalstatus         = row['vitalstatus']
            gbmd1sample.daystodeath         = row['daystodeath']
            gbmd1sample.daystolastfollowup  = row['daystolastfollowup']
            gbmd1sample.gender              = row['gender']
            gbmd1sample.dateofinitialpathologicdiagnosis  = row['dateofinitialpathologicdiagnosis']
            gbmd1sample.radiationtherapy    = row['radiationtherapy']
            gbmd1sample.karnofskyperformancescore        = row['karnofskyperformancescore']
            gbmd1sample.histologicaltype    = row['histologicaltype']
            gbmd1sample.radiationsradiationregimenindication= row['radiationsradiationregimenindication']
            gbmd1sample.race                = row['race']
            gbmd1sample.ethnicity         = row['ethnicity']
            gbmd1sample.neoadjuvanttherapy  = row['neoadjuvanttherapy']
            gbmd1sample.size                = row['size']
            gbmd1sample.link                = row['link']
            gbmd1sample.platform            = row['platform']
            gbmd1sample.save()
