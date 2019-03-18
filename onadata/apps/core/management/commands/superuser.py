from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from onadata.apps.core.models import UserRole
from django.contrib.auth import get_user_model
from django.conf import settings




class Command(BaseCommand):
    help = 'Create superuser'

    def add_arguments(self, parser):
        parser.add_argument('user_name', type=str)

    def handle(self, *args, **options):
        user_name = options['user_name']
        self.stdout.write(user_name)
        super_admin = Group.objects.get(name="super-admin")

        if User.objects.filter(username=user_name).count():
            user = User.objects.get(username=user_name)
            self.stdout.write('user found')
            new_group, created = UserRole.objects.get_or_create(user=user, group=super_admin)
            self.stdout.write('new super admin role created for username')

        else:
            self.stdout.write('username not found.. "%s"',user_name),



 
