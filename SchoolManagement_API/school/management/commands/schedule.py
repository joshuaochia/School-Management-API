from django.core.management.base import BaseCommand
from ...models import Schedule
from faker import Faker
import random

fake = Faker()
days = [
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
    'Saturday', 'Sunday',
]


class Command(BaseCommand):

    """ Add new fake schedule to DB """

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'first',
            type=int,
            help='How many fake schedule you want to add'
            )

    def handle(self, *args, **options):

        success = 0
        fail = 0
        for _ in range(options['first']):
            sched = Schedule.objects.get_or_create(
                start=fake.time(),
                end=fake.time(),
                day=random.choice(days)
            )

            if sched[1]:
                sched[0].save()
                success += 1
                self.stdout.write(self.style.SUCCESS('Creating data...'))

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
