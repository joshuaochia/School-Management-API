from django.core.management.base import BaseCommand
from ...models import Schedule, Subjects, Section, Employees, Courses, School
from faker import Faker
import random
from django.shortcuts import get_object_or_404

fake = Faker()


class Command(BaseCommand):

    """ Adding new fake subject to db """

    teach = Employees.objects.filter(position='Teacher')
    course = Courses.objects.all()
    code = ['MKT', 'BAM', 'ENG', 'PED', 'STEM', 'ABM', 'GAS']
    sched = Schedule.objects.all()
    sec = Section.objects.all()

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'subject',
            type=int,
            help='indicate how many subject you want to generate'
            )

    def handle(self, *args, **options):

        success = 0
        fail = 0
        school = get_object_or_404(School, id=1)

        for _ in range(options['subject']):
            code = f'{random.choice(self.code)} {fake.random_int(min=3,max=3)}'
            sub = Subjects.objects.get_or_create(
                school=school,
                name=fake.company(),
                course=random.choice(self.course),
                code=code,
                unit=fake.random_int(min=1, max=1),
                lab=0,
                cost = fake.random_int(min=3, max=3)
            )

            if sub[1]:
                sub[0].save()
                success += 1
                self.stdout.write(
                    self.style.SUCCESS('Creating data...')
                    )

            else:
                self.stdout.write(
                    self.style.WARNING('Duplicated data found...')
                    )
                fail += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully create {success} data')
            )
        self.stdout.write(
            self.style.WARNING(f'{fail} Duplicated data found')
            )
