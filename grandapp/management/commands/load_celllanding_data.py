from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Celllanding
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
        print("Loading cell landing data!")
        for row in DictReader(open('./data/celllanding.csv')):
            tissuelanding = Celllanding()
            tissuelanding.cancer       = row['cancer']
            tissuelanding.tool         = row['tool']
            tissuelanding.cancerref    = row['cancerref']
            tissuelanding.cancerLink   = row['cancerLink']
            tissuelanding.netzoo       = row['netzoo']
            tissuelanding.netzooLink   = row['netzooLink']
            tissuelanding.netzooRel    = row['netzooRel']
            tissuelanding.network      = row['network']
            tissuelanding.ppi          = row['ppi']
            tissuelanding.ppiLink      = row['ppiLink']
            tissuelanding.motif        = row['motif']
            tissuelanding.expression   = row['expression']
            tissuelanding.expLink      = row['expLink']
            tissuelanding.tfs          = row['tfs']
            tissuelanding.genes        = row['genes']
            tissuelanding.refs         = row['refs']
            tissuelanding.samples      = row['samples']
            tissuelanding.cardref      = row['cardref']
            tissuelanding.script       = row['script']
            tissuelanding.dataset      = row['dataset']
            tissuelanding.refs2        = row['refs2']
            tissuelanding.refs3        = row['refs3']
            tissuelanding.reg          = row['reg']
            tissuelanding.eqtl         = row['eqtl']
            tissuelanding.qbic         = row['qbic']
            tissuelanding.genotype     = row['genotype']
            tissuelanding.motifDesc    = row['motifDesc']
            tissuelanding.tissue       = row['tissue']
            tissuelanding.awsname      = row['awsname']
            tissuelanding.datalink      = row['datalink']
            tissuelanding.vis           = row['vis']
            tissuelanding.save()
