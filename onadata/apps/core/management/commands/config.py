from django.core.management.base import BaseCommand, CommandError
from onadata.apps.core.models import Config


class Command(BaseCommand):
    help = 'Create Config'

    def handle(self, *args, **options):
    	if not Config.objects.count():
    		c = Config(available_version=0.00, updates='first config')
    		c.save()
