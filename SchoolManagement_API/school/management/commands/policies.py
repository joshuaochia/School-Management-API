from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from school.models import Policies, School
from faker import Faker

fake = Faker()


class Command(BaseCommand):

    help = 'Populate fake Policies data'

    def add_arguments(self, parser):
        parser.add_argument('first', type=int, help='A number less than 100')

    def handle(self, *args, **options):

        school = get_object_or_404(School, pk=1)
        success = 0

        for _ in range(options['first']):
            policy = Policies.objects.get_or_create(
                policy=fake.text(),
                school=school
            )

            if policy[1]:
                policy[0].save()
                self.stdout.write(self.style.SUCCESS('Creating data....'))
                success += 1
            else:
                self.stdout.write(
                    self.style.WARNING('Duplicated data found..')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'Success, created {success} fake data')
            )
