from django.core.management.base import BaseCommand, CommandError
import pandas as pd
import sys
import argparse
from onadata.apps.core.models import District, Municipality

class Command(BaseCommand):
    help = 'Create Districts and municipalities'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_csv(sys.argv[3]).fillna(value='')
        try:
            total = df['FIRST_DIST'].count()
            for row in range(total):
                district, created = District.objects.get_or_create(name=df['FIRST_DIST'][row])
                print(district)
                municipality = Municipality.objects.get_or_create(district=district, name=df['FIRST_GaPa'][row])
            print("successfully created")

        except Exception as e:
            print(e)

