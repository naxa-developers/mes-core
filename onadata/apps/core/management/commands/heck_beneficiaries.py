from django.core.management.base import BaseCommand, CommandError
import sys
import argparse
from onadata.apps.core.models import Submission, Beneficiary, District, Municipality, Cluster
import ast
import json
import pandas as pd
from django.db.models import Q

class Command(BaseCommand):
    help = 'Update beneficiaries'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value="")
        name = []
        try:
            total = df['SN' ].count()
            for row in range(total):
                name.append(df['Name of Beneficiries '])
            
            print(Beneficiary.objects.filter(name__in=name).count())

        except Exception as e:
            print(e)