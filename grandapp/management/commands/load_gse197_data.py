from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Gse197sample
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
        for row in DictReader(open('./static/data/GSE19783_phenotype.csv')):
            gse197sample = Gse197sample()
            gse197sample.sample        = row['sample']
            gse197sample.geoid         = row['geo_accession']
            gse197sample.source        = row['source_name_ch1']
            gse197sample.subtype       = row['characteristics_ch1_2']
            gse197sample.mutation      = row['characteristics_ch1_3']
            gse197sample.vital_status  = row['death status:ch1']
            gse197sample.time_to_event = row['disease free survival time (months):ch1']
            gse197sample.estrogen      = row['estrogen_receptor_status_ch1']
            gse197sample.her2          = row['her2 _fish_status_ch1']
            gse197sample.gender        = 'Female'
            gse197sample.tumor_location          = row['disease state:ch1']
            gse197sample.size          = row['size']
            gse197sample.link          = row['link']
            gse197sample.sampleclean   = row['sampleclean']
            gse197sample.save()
