from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Genelanding
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
        print("Loading gene data!")
        for row in DictReader(open('./data/GSE92742_Broad_LINCS_gene_info.csv')):
            genelanding = Genelanding()
            genelanding.pr_gene_id     = row['pr_gene_id']
            genelanding.pr_gene_symbol = row['pr_gene_symbol']
            genelanding.pr_gene_title  = row['pr_gene_title']
            genelanding.pr_is_lm       = row['pr_is_lm']
            genelanding.pr_is_bing     = row['pr_is_bing']
            genelanding.save()
