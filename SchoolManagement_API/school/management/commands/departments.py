from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from school.models import Department, School
from faker import Faker

fake = Faker()


class Command(BaseCommand):

    help = 'Populate fake Departments data'

    def add_arguments(self, parser):
        parser.add_argument('first', type=int, help='A number less than 100')

    def handle(self, *args, **options):

        school = get_object_or_404(School, pk=1)
        success = 0
        fail = 0

        for i in range(options['first']):
            department = Department.objects.get_or_create(
                name=f'Department of {fake.company()}',
                school=school
            )

            if department[1]:
                department.save()
                self.stdout.write(
                    self.style.SUCCESS('Creating data...')
                    )
                success += 1

            else:
                self.stdout.write(
                    self.style.WARNING('Duplicate data found..')
                    )
                fail += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {success} fake data')
            )
        self.stdout.write(
            self.style.WARNING(f'Found {fail} duplicated fake data')
            )
