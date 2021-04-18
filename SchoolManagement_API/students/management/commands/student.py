from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from students.models import Students, Subjects, StudentSubject
from faker import Faker
from school.models import School, Courses
from django.contrib.auth import get_user_model
import random

fake = Faker()


class Command(BaseCommand):

    """
    Fake data generator for students and add how many subject
    you want them to have
    """
    help = 'This the help for students fake populating'
    course = Courses.objects.all()
    sub = Subjects.objects.all()

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'student',
            type=int,
            help='How many unique students'
            )
        parser.add_argument(
            'subject',
            type=int,
            help='How many unique subject per student'
            )

    def handle(self, *args, **options):

        success = 0
        fail = 0
        for _ in range(options['first']):

            school = get_object_or_404(School, pk=1)
            user = get_user_model().objects.create_user(
                email=fake.email(),
                first_name=fake.first_name(),
                middle_name=fake.last_name(),
                last_name=fake.last_name(),
                password=fake.password(),
                )
            student = Students.objects.get_or_create(
                user=user,
                school=school,
                course=random.choice(self.course),
                bday=fake.date(),
                country='Philippines',
                city=fake.city(),
                zip_code=fake.random_int(min=3, max=5),
                sex=random.choice(['Male', 'Femail']),
                civil_status=random.choice(['Married', 'Single']),
                school_yr=fake.year(),
                sem=random.choice(['First', 'Second'])
            )

            if student[1]:
                student[0].save()
                self.stdout.write(self.style.SUCCESS('Creating data..'))
                success += 1

                for _ in range(options['two']):
                    StudentSubject.objects.get_or_create(
                        student=student[0],
                        subject=random.choice(self.sub)
                        )

            else:
                self.stdout.write(
                    self.style.WARNING('Duplicated data found..')
                    )
                fail += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully create {success} data')
            )
        self.stdout.write(
            self.style.WARNING(f'{fail} Duplicated data found')
            )
