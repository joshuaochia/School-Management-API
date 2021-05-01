from django.core.management.base import BaseCommand
from ...models import Section
from faker import Faker

fake = Faker()


class Command(BaseCommand):

    """ Add new fake section to DB """

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            'section',
            type=int,
            help='How many fake section you want to add'
            )

    def handle(self, *args, **options):

        success = 0
        fail = 0
        for _ in range(options['section']):
            sec = Section.objects.get_or_create(
                name=fake.company(),
                code=fake.random_int(min=3, max=6)
            )

            if sec[1]:
                sec[0].save()
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
