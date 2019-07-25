from django.core.management.base import BaseCommand, CommandError
import sys
import argparse
from onadata.apps.logger.models import XForm, Instance
from onadata.apps.core.models import Submission
import ast
import json


class Command(BaseCommand):
    help = 'Create Districts and municipalities'

    def handle(self, *args, **options):
        id_strings = ['adBbmShANEfCgZwP676nXg', 'aDpShE5ecJqLN4AVmt69Tj']
        for id_string in id_strings:
            try:
                xf = XForm.objects.get(id_string=id_string)
                j = json.loads(str(xf.json))
                children = j.get('children')
                for item in children:
                    if item['type'] == 'acknowledge':
                        instances = Instance.objects.filter(xform_id=xf.id)
                        for instance in instances:
                            if instance.json.get(item['name']) == 'OK':
                                Submission.objects.filter(instance=instance).update(status='approved')
                                print('Submission approved for submission id: ', instance.id)
            except Exception as e:
                print(e)
