from django.core.management.base import BaseCommand, CommandError

from api.models import Role, Perm


class Command(BaseCommand):
    help = 'Add new role to database'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--name', type=str)
        parser.add_argument('-p', '--perm', type=str)

    def handle(self, *args, **options):
        name = options.get('name')
        perm = options.get('perm')

        if not name:
            raise CommandError('Name is required')

        role, created = Role.objects.get_or_create(name=name)
        if created:
            self.stdout.write(self.style.SUCCESS(f'New role added to database ({name})'))
        else:
            self.stdout.write(self.style.WARNING(f'Role already exists ({name})'))

        if perm:
            method, path = perm.split(',')
            new_perm, _ = Perm.objects.get_or_create(method=method, path=path)
            role.perms.add(new_perm)
            self.stdout.write(self.style.SUCCESS(f'Perm added to role ({perm}, {name})'))
