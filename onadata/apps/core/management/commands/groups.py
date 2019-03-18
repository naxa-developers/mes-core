from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create default groups'

    def handle(self, *args, **options):
        group_list = ['super-admin', 'project-manager', 'project-management-unit', 'project-coordinator', 'social-mobilizer']
        for group in group_list:
            new_group, created = Group.objects.get_or_create(name=group)
            self.stdout.write('Successfully created group .. "%s"' % group)


