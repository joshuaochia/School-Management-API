from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from school.models import Employees, School, Department
from faker import Faker
import random
from django.contrib.auth import get_user_model

fake = Faker()


class Command(BaseCommand):

    help = 'Populate fake Employees data'
    created_by = get_user_model().objects.filter(is_superuser=True)

    deparment = Department.objects.all()
    sex = ['Male', 'Female']
    position = ['Teacher', 'Maintainance', 'Department Head', 'IT']


    def add_arguments(self, parser):
        parser.add_argument('first', type=int, help='A number less than 100')


    def handle(self, *args, **options):
        
        school = get_object_or_404(School, pk=1)


        success = 0
        fail = 0
        for i in range(options['first']):
            
            user = get_user_model().objects.create_user(
                email = fake.email(),
                first_name = fake.first_name(),
                middle_name = fake.last_name(),
                last_name = fake.last_name(),
                password = fake.password()
            )
            created_by = random.choice(self.created_by)
            department = random.choice(self.deparment)
            data = Employees.objects.get_or_create(
                user = user,
                created_by = created_by,
                school = school,
                department = department,
                bday = fake.date(),
                city = fake.city(),
                position = random.choice(self.position),
                sex = random.choice(self.sex)
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