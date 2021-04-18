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

        for i in range(options['first']):
            department = Department.objects.get_or_create(
                name = f'Department of {fake.company()}',
                school = school
            )[0]
            department.save()
            self.stdout.write(f'Creating data... {int(i)}')

            q =+ int(i)

        self.stdout.write(self.style.SUCCESS(f'Success, created {q+1} fake data'))