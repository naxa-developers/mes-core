from django.core.management.base import BaseCommand, CommandError
import sys
import argparse
from onadata.apps.core.models import Submission, Beneficiary, District, Municipality, Cluster
import ast
import json
import pandas as pd


class Command(BaseCommand):
    help = 'Update beneficiaries'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value="")
        try:
            total = df['SN' ].count()
            for row in range(total):
                municipality = Municipality.objects.get(name=df['Municipality'][row])
                district = municipality.district
                name = df['Name of Beneficiries '][row]
                nra_card_no = df.get('NRA CARD No', '')[row]
                print(nra_card_no)
                ward = int(df.get('Ward', '')[row])
                try:
                    cluster = Cluster.objects.get(name=df['Cluster'][row])
                except:
                    cluster = None
                houseType = df.get('Types of Houses', '')[row]
                category = df.get('Category', '')[row]
                vulnerabilityType = df.get('Tyeps of Vulnerability', '')[row]
                tranch = df.get('Tranches Progress', '')[row]
                remarks = df.get('Remarks', '')[row]

                if cluster:
                    beneficiary, created = Beneficiary.objects.get_or_create(
                        name=name,
                        district=district,
                        municipality=municipality,
                        cluster=cluster,
                        ward_no=ward,
                        Type=category
                    )
                    if created:
                        print(name)

                    beneficiary.nra_card_number = nra_card_no
                    beneficiary.Typesofhouse = houseType
                    beneficiary.GovernmentTranch = tranch
                    beneficiary.vulnerabilityType = vulnerabilityType
                    beneficiary.Remarks = remarks
                    
                    beneficiary.save()
                else:
                    beneficiary, created = Beneficiary.objects.get_or_create(
                        name=name,
                        district=district,
                        municipality=municipality,
                        ward_no=ward,
                        Type=category
                    )

                    beneficiary.nra_card_number = nra_card_no
                    beneficiary.Typesofhouse = houseType
                    beneficiary.GovernmentTranch = tranch
                    beneficiary.vulnerabilityType = vulnerabilityType
                    beneficiary.Remarks = remarks
                    
                    beneficiary.save()

            print('success')
        except Exception as e:
            print(e)