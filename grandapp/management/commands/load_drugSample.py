from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from grandapp.models import Drugsample
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
        print("Loading drug sample data!")
        for row in DictReader(open('./data/drug_vars_difftar_genetar_tfexp_geneexp_clean.csv')):
            drugsample = Drugsample()
            drugsample.sig_id     = row['sig_id']
            drugsample.pert_iname = row['pert_iname']
            drugsample.cell_id    = row['cell_id']
            drugsample.pert_idose = row['pert_idose']
            drugsample.pert_itime = row['pert_itime']
            drugsample.distil_nsample = row['distil_nsample']
            drugsample.cell_type      = row['cell_type']
            drugsample.modification   = row['modification']
            drugsample.sample_type    = row['sample_type']
            drugsample.primary_site   = row['primary_site']
            drugsample.subtype   = row['subtype']
            drugsample.original_growth_pattern = row['original_growth_pattern']
            drugsample.donor_age = row['donor_age']
            drugsample.donor_sex = row['donor_sex']
            drugsample.donor_ethnicity = row['donor_ethnicity']
            drugsample.infl      = row['infl']
            drugsample.links     = row['links']
            drugsample.linksTF   = row['linksTF']
            drugsample.diffexp       = row['diffexp']
            drugsample.diffexpgenes  = row['diffexpgenes']
            drugsample.difftar       = row['difftar']
            drugsample.difftargenes  = row['difftargenes']
            drugsample.cleannames    = row['cleannames']
            drugsample.save()
