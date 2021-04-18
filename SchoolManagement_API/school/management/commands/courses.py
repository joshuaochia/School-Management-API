from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from school.models import Courses, School
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):

    help = 'Populate fake Policies data'
    course = ['BS','BSBA', 'AB','MA','MS']
    major = [
    'Marketing', 'Finance', 'ME', 'CE', 'Accountancy', 'Education', 'Fine Arts',
    'Forestry', 'Legal Management', 'Architecture', 'AE', 'IE', 'COE', 'EE', 'GE'
]

    def add_arguments(self, parser):
        parser.add_argument('first', type=int, help='A number less than 100')


    def handle(self, *args, **options):
        
        school = get_object_or_404(School, pk=1)

        success = 0
        fail = 0
        for i in range(options['first']):
            course = random.choice(self.course)
            major = random.choice(self.major)
            data = Courses.objects.get_or_create(
                course = course,
                school = school,
                major = major
            )
            if data[1]:
                data[0].save()
                self.stdout.write(self.style.SUCCESS('Creating data...'))
                success += 1
            else:
                self.stdout.write(self.style.WARNING('Duplicate data found..'))
                fail += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {success} fake data'))
        self.stdout.write(self.style.WARNING(f'Found {fail} duplicated fake data'))