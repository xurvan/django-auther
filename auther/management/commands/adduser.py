import bcrypt
from django.core.management.base import BaseCommand, CommandError

from api.models import Profile, Role


class Command(BaseCommand):
    help = 'Add new user to database'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--name', type=str)
        parser.add_argument('-u', '--username', type=str)
        parser.add_argument('-p', '--password', type=str)
        parser.add_argument('-r', '--role', type=str)

    def handle(self, *args, **options):
        name = options.get('name')
        username = options.get('username')
        password = options.get('password')
        role = options.get('role')

        if not name:
            raise CommandError('Name is required')
        if not username:
            raise CommandError('Username is required')
        if not password:
            raise CommandError('Password is required')

        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = Profile(name=name, username=username, password=password)
        user.save(force_insert=True)
        self.stdout.write(self.style.SUCCESS(f'New user added to database ({username})'))

        if role:
            new_role, _ = Role.objects.get_or_create(name=role)
            user.roles.add(new_role)
            self.stdout.write(self.style.SUCCESS(f'New role added to user ({role}, {username})'))
